import time
import errno
from six.moves import cPickle as pickle
import six
import socket


def handle_eintr(func):
    """Temporary fix until pep 475 is implemented"""
    def new_func(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except EnvironmentError as e:
                if e.errno != errno.EINTR:
                    raise
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    return new_func


def create_listen_socket():
    listensock = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listensock.bind(("127.0.0.1", 0))
    listensock.listen(128)
    listensock.setblocking(False)
    return listensock


def int2bytes(int_, byte_count=1):
    int_ = int_ if int_ is not None else 0
    bytes_ = b"".join([
        six.int2byte((int_ >> (8 * i)) & 0xFF)
        for i in range(byte_count - 1, -1, -1)])
    return bytes_


def bytes2int(bytes_):
    int_ = 0
    for i in range(len(bytes_)):
        int_ <<= 8
        int_ |= six.indexbytes(bytes_, i)
    return int_


class SocketClient(object):
    _poll_rate = 0.1

    def __init__(self, host=None, port=None, sock=None, timeout=None):
        if sock is not None:
            self._sock = sock
        elif host is not None and port is not None:
            self._sock = handle_eintr(socket.create_connection)(host, port)
            self._sock.settimeout(self._poll_rate)
            self.timeout = timeout or 10
        else:
            raise Exception("No valid host/port/socket")
        self.buf = b""

    def readline(self):
        start = time.time()
        while time.time() - start < self.timeout:
            index = self.buf.find(b"\n") + 1
            if index != -1:
                break
            self.buf += self._sock.read()
        else:
            raise socket.timeout
        line, self.buf = self.buf[:index], self.buf[index:]
        return line

    def read(self):
        read = b""
        try:
            read += self._sock.recv(2**32)
        except socket.timeout:
            pass
        return read

    def send(self, data):
        self._sock.send(data)

    def read_n(self, n):
        start = time.time()
        while time.time() - start < self.timeout:
            if len(self.buf) >= n:
                break
            self.buf += self._sock.read()
        else:
            raise socket.timeout
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def recv_obj(self):
        size = bytes2int(self.read_n(4))
        return pickle.loads(self.read_n(size))

    def send_obj(self, obj):
        data = pickle.dumps(obj)
        self.send(int2bytes(len(data), 4) + data)

    def fileno(self, *args):
        return self._sock.fileno(*args)
