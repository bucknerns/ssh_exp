import sys
import base64

import six

__all__ = ['PY2', 'string_types', 'integer_types', 'text_type', 'bytes_types', 'bytes', 'long', 'input',
           'decodebytes', 'encodebytes', 'bytestring', 'byte_ord', 'byte_chr', 'byte_mask',
           'b', 'u', 'b2s', 'StringIO', 'BytesIO', 'is_callable', 'MAXSIZE', 'next', 'builtins']

string_types = six.string_types
text_type = six.text_type
bytes = bytes_types = six.binary_type
integer_types = six.integer_types
builtins = six.moves.builtins
PY2 = six.PY2
byte_chr = six.int2byte
b = six.b
u = six.u
is_callable = six.callable
next = six.next
StringIO = six.moves.cStringIO

# will use cStringIO which is faster
BytesIO = StringIO if PY2 else six.BytesIO

input = six.moves.input
MAXSIZE = six.MAXSIZE

def byte_ord(c):
    if not isinstance(c, integer_types):
        c = ord(c)
    return c

if PY2:
    long = long
    decodebytes = base64.decodestring
    encodebytes = base64.encodestring

    def bytestring(s):  # NOQA
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    def byte_mask(c, mask):
        return chr(ord(c) & mask)
else:
    long = type("long", (int,), {})
    decodebytes = base64.decodebytes
    encodebytes = base64.encodebytes

    def bytestring(s):
        return s

    def byte_mask(c, mask):
        assert isinstance(c, int)
        return struct.pack('B', c & mask)
