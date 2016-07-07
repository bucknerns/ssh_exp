from multiprocessing import Process
from six.moves import cPickle as pickle
import six
import socket

try:
    FAMILY = socket.AF_UNIX
except NameError:
    FAMILY = socket.AF_INET
TYPE = socket.SOCK_STREAM
PROTO = socket.IPPROTO_IP
LOCALHOST = '127.0.0.1'


def from_fd(fd):
    return socket.fromfd(fd, FAMILY, TYPE, PROTO)


def socketpair():
    """Wraps socketpair() to support Windows using local ephemeral ports
       This is a mix of python 3.5 socketpair on windows with a goal of making
       selectable communication cross platform"""
    try:
        return socket.socketpair(FAMILY, TYPE, PROTO)
    except:
        host = LOCALHOST
        # creates new socket on connect
        listensock = socket(FAMILY, TYPE, PROTO)
        listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            listensock.bind((host, 0))
            listensock.listen()
            addr, port = listensock.getsockname()
            csock = socket(FAMILY, TYPE, PROTO)
            try:
                csock.setblocking(False)
                csock.connect((addr, port))
                csock.setblocking(True)
                ssock, _ = listensock.accept()
            except:
                csock.close()
                raise
        finally:
            listensock.close()
        return (ssock, csock)


def write_int(int_, byte_count=1):
    int_ = int_ if int_ is not None else 0
    bytes_ = b"".join([
        six.int2byte((int_ >> (8 * i)) & 0xFF)
        for i in range(byte_count - 1, -1, -1)])
    return bytes_


def read_int(bytes_):
    int_ = 0
    for i in range(len(bytes_)):
        int_ <<= 8
        int_ |= six.indexbytes(bytes_, i)
    return int_


def send_obj(socket, obj):
    data = pickle.dumps(obj)
    socket.send(write_int(len(data), 4) + data)


def recv_obj(socket):
    size = read_int(socket.recv(4))
    data = socket.recv(size)
    return pickle.loads(data)


class Client(Process):
    """This class runs as a process and does the test running"""
    def __init__(self, socket_):
        super(Client, self).__init__()
        self.socket = socket_

    def run(self):
        send_obj(self.socket, {"cmd": "print", "data": "message recieved from client"})
        ret_val = recv_obj(self.socket)
        print(ret_val)
        print("client exited")


class Server(Process):
    """This class runs as a process and does the test running"""
    def __init__(self, socket_):
        super(Server, self).__init__()
        self.socket = socket_

    def run(self):
        done_stuff = False
        while True:
            data = recv_obj(self.socket)
            if data is None and done_stuff:
                break
            elif data is None:
                continue
            elif data.get("cmd") == "print":
                print(data.get("data"))
                send_obj(self.socket, "message recieved from server")
                done_stuff = True
        print "server exited"


def main():
    # create sockets
    server_socket, client_socket = socketpair()

    proc1 = Client(client_socket)
    proc2 = Server(server_socket)
    print proc2.socket
    proc2.start()
    proc1.start()
    proc1.join()
    print("joined client")
    send_obj(client_socket, None)
    print("sent None to server")
    proc2.join()
    print("joined proc2")

if __name__ == "__main__":
    main()
