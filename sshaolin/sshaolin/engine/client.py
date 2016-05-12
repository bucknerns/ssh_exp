import six
import socket
import errno


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


def class_eintr(cls):
    for name, value in vars(cls).items():
        if six.callable(value):
            setattr(name, handle_eintr(value))
    return cls


@class_eintr
class SSHMessageClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _connect(self, sock=None):
        self._sock = sock or handle_eintr(socket.create_connection)(
            (self.host, self.port))
        self._sock.settimeout(0.1)  # poll rate

"""
checks version
    buf = buf.split(" ", 1)[0]
    try:
        _, version, client = buf.split("-", 2)
    except ValueError:
        raise SSHException('Invalid SSH banner')
"""