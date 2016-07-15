from six.moves import cPickle as pickle
import six
from select import select
from sshaolin.engine import socket_helper
from threading import Thread
import errno




class SSHMessageClient(Thread):
    def __init__(self, host, port, sock=None):
        self.listen_sock = socket_helper.create_listen_socket()
        self.listen_port = self.listensock.getsockname()[1]
        self.ssh_sock = socket_helper.SocketClient(
            host=host, port=port, sock=sock)
        self.sockets = [self.listen_sock, self.ssh_sock]
        self.host = host
        self.port = port

    def run(self):
        while True:
            read, _, _ = select(self.sockets, [], [])
            for s in read:
                if s is self.listensock:
                    new_sock = socket_helper.SocketClient(sock=s.accept()[0])
                    self.sockets.append(new_sock)
                    continue
                data = recv_obj(s)
                if data is None:
                    print("server exited")
                    exit(0)
                elif data.get("cmd") == "print":
                    print(data.get("data"))
                    send_obj(s, "Hello Client!")

