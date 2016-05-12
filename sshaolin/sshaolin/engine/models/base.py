import six


class BaseModel(object):
    def __init__(self, kwargs):
        for k, v in kwargs.items():
            if k not in ["self"]:
                setattr(self, k, v)

    @staticmethod
    def _write_int(int_, byte_count=1):
        int_ = int_ if int_ is not None else 0
        bytes_ = b"".join([
            six.int2byte((int_ >> (8 * i)) & 0xFF)
            for i in range(byte_count - 1, -1, -1)])
        return bytes_

    @classmethod
    def _write_list(cls, list_):
        list_ = list_ or []
        tmp = b""
        if list_:
            for string in list_[:-1]:
                tmp += six.b(string)
                tmp += b","
            tmp += six.b(list_[-1])
        return cls._write_string(tmp)

    @classmethod
    def _write_string(cls, string):
        string = six.b(string or b"")
        return cls._write_int(len(string), 4) + string

    @staticmethod
    def _write_bool(value):
        if value:
            return b"\x01"
        else:
            return b"\x00"

    def asbytes(self):
        print([self.to_bytes()])
        return self.to_bytes()


class PacketModel(BaseModel):
    MAX_SIZE = 35000

    def __init__(self, model, block_size, compression_method=None):
        super(PacketModel, self).__init__(locals())
        self.block_size = block_size if block_size >= 8 else 8

    def to_bytes(self):
        payload = self.model.to_bytes()
        if len(payload) > self.MAX_SIZE:
            self._log.warning("Packet oversized")
        if self.compression_method is not None:
            payload = self.compression_method(self.payload)

        size = len(payload) + 5
        padding_size = size % self.block_size
        padding_size = (
            padding_size if padding_size >= 4 else
            size % self.block_size + self.block_size)


