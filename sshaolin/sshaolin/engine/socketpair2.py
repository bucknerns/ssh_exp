from threading import Thread
import six
import socket
from select import select
from six.moves import cPickle as pickle


def create_listen_socket():
    listensock = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    listensock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listensock.bind(("127.0.0.1", 0))
    listensock.listen(128)
    listensock.setblocking(False)
    return listensock


def connect_socket(port):
    try:
        csock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        csock.connect(("127.0.0.1", port))
    except:
        csock.close()
        raise
    return csock


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


class Client(Thread):
    """This class runs as a process and does the test running"""
    def __init__(self, port):
        super(Client, self).__init__()
        self.socket = connect_socket(port)

    def run(self):
        send_obj(self.socket, {"cmd": "print", "data": "Hello Server"})
        ret_val = recv_obj(self.socket)
        print(ret_val)
        print("client exited")


class Server(Thread):
    """This class runs as a process and does the test running"""
    def __init__(self):
        super(Server, self).__init__()
        self.listensock = create_listen_socket()
        self.port = self.listensock.getsockname()[1]
        self.sockets = [self.listensock]

    def run(self):

        while True:
            read, _, _ = select(self.sockets, [], [])
            for s in read:
                if s is self.listensock:
                    new_sock, _ = s.accept()
                    self.sockets.append(new_sock)
                    continue
                data = recv_obj(s)
                if data is None:
                    print("server exited")
                    exit(0)
                elif data.get("cmd") == "print":
                    print(data.get("data"))
                    send_obj(s, "Hello Client!")


def main():
    server = Server()
    server.start()
    print(server.port)
    proc1 = Client(server.port)
    proc1.start()
    proc1.join()
    print("joined proc1")
    server_connection = connect_socket(server.port)
    send_obj(server_connection, None)
    print("sent None to server")
    server.join()
    print("joined proc2")

if __name__ == "__main__":
    main()
