# Copyright (C) 2003-2006 Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

import stat
import time
from paramiko.common import x80000000, o700, o70, xffffffff
from paramiko.py3compat import long, b


class SFTPAttributes (object):
    """
    Representation of the attributes of a file (or proxied file) for SFTP in
    client or server mode.  It attemps to mirror the object returned by
    `os.stat` as closely as possible, so it may have the following fields,
    with the same meanings as those returned by an `os.stat` object:

        - ``st_size``
        - ``st_uid``
        - ``st_gid``
        - ``st_mode``
        - ``st_atime``
        - ``st_mtime``

    Because SFTP allows flags to have other arbitrary named attributes, these
    are stored in a dict named ``attr``.  Occasionally, the filename is also
    stored, in ``filename``.
    """

    FLAG_SIZE = 1
    FLAG_UIDGID = 2
    FLAG_PERMISSIONS = 4
    FLAG_AMTIME = 8
    FLAG_EXTENDED = x80000000

    def __init__(self):
        """
        Create a new (empty) SFTPAttributes object.  All fields will be empty.
        """
        self._flags = 0
        self.st_size = None
        self.st_uid = None
        self.st_gid = None
        self.st_mode = None
        self.st_atime = None
        self.st_mtime = None
        self.attr = {}

    @classmethod
    def from_stat(cls, obj, filename=None):
        """
        Create an `.SFTPAttributes` object from an existing ``stat`` object (an
        object returned by `os.stat`).

        :param object obj: an object returned by `os.stat` (or equivalent).
        :param str filename: the filename associated with this file.
        :return: new `.SFTPAttributes` object with the same attribute fields.
        """
        attr = cls()
        attr.st_size = obj.st_size
        attr.st_uid = obj.st_uid
        attr.st_gid = obj.st_gid
        attr.st_mode = obj.st_mode
        attr.st_atime = obj.st_atime
        attr.st_mtime = obj.st_mtime
        if filename is not None:
            attr.filename = filename
        return attr

    def __repr__(self):
        return '<SFTPAttributes: %s>' % self._debug_str()

    ###  internals...
    @classmethod
    def _from_msg(cls, msg, filename=None, longname=None):
        attr = cls()
        attr._unpack(msg)
        if filename is not None:
            attr.filename = filename
        if longname is not None:
            attr.longname = longname
        return attr

    def _unpack(self, msg):
        self._flags = msg.get_int()
        if self._flags & self.FLAG_SIZE:
            self.st_size = msg.get_int64()
        if self._flags & self.FLAG_UIDGID:
            self.st_uid = msg.get_int()
            self.st_gid = msg.get_int()
        if self._flags & self.FLAG_PERMISSIONS:
            self.st_mode = msg.get_int()
        if self._flags & self.FLAG_AMTIME:
            self.st_atime = msg.get_int()
            self.st_mtime = msg.get_int()
        if self._flags & self.FLAG_EXTENDED:
            count = msg.get_int()
            for i in range(count):
                self.attr[msg.get_string()] = msg.get_string()

    def _pack(self, msg):
        self._flags = 0
        if self.st_size is not None:
            self._flags |= self.FLAG_SIZE
        if (self.st_uid is not None) and (self.st_gid is not None):
            self._flags |= self.FLAG_UIDGID
        if self.st_mode is not None:
            self._flags |= self.FLAG_PERMISSIONS
        if (self.st_atime is not None) and (self.st_mtime is not None):
            self._flags |= self.FLAG_AMTIME
        if len(self.attr) > 0:
            self._flags |= self.FLAG_EXTENDED
        msg.add_int(self._flags)
        if self._flags & self.FLAG_SIZE:
            msg.add_int64(self.st_size)
        if self._flags & self.FLAG_UIDGID:
            msg.add_int(self.st_uid)
            msg.add_int(self.st_gid)
        if self._flags & self.FLAG_PERMISSIONS:
            msg.add_int(self.st_mode)
        if self._flags & self.FLAG_AMTIME:
            # throw away any fractional seconds
            msg.add_int(long(self.st_atime))
            msg.add_int(long(self.st_mtime))
        if self._flags & self.FLAG_EXTENDED:
            msg.add_int(len(self.attr))
            for key, val in self.attr.items():
                msg.add_string(key)
                msg.add_string(val)
        return

    def _debug_str(self):
        out = '[size={size}, uid={uid}, gid={gid}, mode="{mode}", '
        out += 'atime="{atime}", mtime="{mtime}"'
        out = out.format(
            size=self.st_size, uid=self.st_uid, gid=self.st_gid,
            mode=self._perm_string, atime=self._datestr(self.st_atime),
            mtime=self._datestr(self.st_mtime))
        for k, v in self.attr.items():
            out += ", {0}={1}".format(k, v)
        out += ']'
        return out

    @staticmethod
    def _rwx(n, suid, sticky=False):
        index = (4 if suid and sticky else 2 if suid else 0) + (n & 1)
        out = ("r" if n & 4 else "-") + ("w" if n & 2 else "-")
        return out + "-xSsTt"[index]

    @property
    def _perm_string(self):
        mode = self. st_mode
        if mode is None:
            return "?---------"
        kind = stat.S_IFMT(mode)
        mapping = {
            stat.S_IFIFO: 'p', stat.S_IFCHR: 'c', stat.S_IFDIR: 'd',
            stat.S_IFBLK: 'b', stat.S_IFREG: '-', stat.S_IFLNK: 'l',
            stat.S_IFSOCK: 's'}
        out = mapping.get(kind, "?")
        out += self._rwx(mode >> 6 & 7, mode & stat.S_ISUID)
        out += self._rwx(mode >> 3 & 7, mode & stat.S_ISGID)
        out += self._rwx(mode & 7, mode & stat.S_ISVTX, True)
        return out

    def _datestr(self, xtime):
        if (xtime is None) or (xtime == xffffffff):
            return '(unknown date)'
        format_ = "%d %b %H:%M"
        if abs(time.time() - xtime) > 15552000: # 6 months
            format_ = "%d %b %Y"
        return time.strftime(format_, time.localtime(xtime))

    def __str__(self):
        """create a unix-style long description of the file (like ls -l)"""
        datestr = self._datestr(self.st_mtime)
        filename = getattr(self, 'filename', '?')
        uid = self.st_uid or 0
        gid = self.st_gid or 0
        size = self.st_size or 0

        return "{0}   1 {1:<8} {2:<8} {3:8} {4:<12} {5}".format(
            self._perm_string, uid, gid, size, datestr, filename)

    def asbytes(self):
        return b(str(self))
