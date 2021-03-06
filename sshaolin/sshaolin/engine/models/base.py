import six


messages = {}


class MessageType(type):
    def __new__(cls, cls_name, cls_parents, cls_attr):
        new_class = super(MessageType, cls).__new__(
            cls, cls_name, cls_parents, cls_attr)

        if getattr(new_class, "message_id", False):
            if new_class.message_id in messages:
                msg = "Message id {}".format(new_class.message_id)
                raise Exception(msg)
            messages[new_class.message_id] = new_class
        return new_class


@six.add_metaclass(MessageType)
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
                print(string)
                tmp += bytes(string)
                tmp += b","
            tmp += bytes(list_[-1])
        return cls._write_string(tmp)

    @classmethod
    def _write_string(cls, string):
        string = string or b""
        return cls._write_int(len(string), 4) + string

    @staticmethod
    def _write_bool(value):
        if value:
            return b"\x01"
        else:
            return b"\x00"

    def asbytes(self):
        return self.to_bytes()

    @classmethod
    def from_message(cls, message, type_=None):
        type_ = type_ or cls.message_id
        bytes_ = six.BytesIO(message)
        model = messages[int(type_)].from_bytes(bytes_)
        current_pos = bytes_.tell()
        bytes_.seek(0)
        model._raw = six.int2byte(model.message_id) + bytes_.read(current_pos)
        return model

    @classmethod
    def _get_list(cls, bytes_):
        num_bytes = cls._get_int(4, bytes_)
        return bytes_.read(num_bytes).split(b",")

    @staticmethod
    def _get_bytes(n, bytes_):
        return bytes_.read(n)

    @staticmethod
    def _get_int(n, bytes_):
        int_bytes = bytes_.read(n)
        return sum([
            six.byte2int(int_bytes[i:]) << (8 * x) for i, x in enumerate(
                range(n - 1, -1, -1))])

    @classmethod
    def _get_bool(cls, bytes_):
        return bool(cls._get_int(1, bytes_))


class PacketModel(BaseModel):
    """
    uint32    packet_length
    byte      padding_length
    byte[n1]  payload; n1 = packet_length - padding_length - 1
    byte[padding_length]  random padding
    byte[m]   mac (Message Authentication Code - MAC); m = mac_length

    packet_length
        The length of the packet in bytes, not including 'mac' or the
        'packet_length' field itself.

    padding_length
        Length of 'random padding' (bytes).

    payload
        The useful contents of the packet.  If compression has been
        negotiated, this field is compressed.  Initially, compression
        MUST be "none".

    random padding
        Arbitrary-length padding, such that the total length of
        (packet_length || padding_length || payload || random padding)
        is a multiple of the cipher block size or 8, whichever is
        larger.  There MUST be at least four bytes of padding.  The
        padding SHOULD consist of random bytes.  The maximum amount of
        padding is 255 bytes.

    """
    MAX_SIZE = 35000

    def __init__(self, model, block_size, compression_method=None):
        super(PacketModel, self).__init__(locals())
        self.block_size = block_size if block_size >= 8 else 8
        self.model = model

    def to_bytes(self):
        payload = self.model.to_bytes()
        if len(payload) > self.MAX_SIZE:
            self._log.warning("Packet oversized")
        if self.compression_method is not None:
            payload = self.compression_method(self.payload)

        padding_size = (len(payload) + 5) % self.block_size
        if padding_size < 4:
            padding_size += self.block_size
