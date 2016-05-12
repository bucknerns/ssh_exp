import os
import six

from sshaolin.engine.constants import MessageIDs
from sshaolin.engine.models.base import BaseModel


class KexInitModel(BaseModel):
    """
      byte         SSH_MSG_KEXINIT
      byte[16]     cookie (random bytes)
      name-list    kex_algorithms
      name-list    server_host_key_algorithms
      name-list    encryption_algorithms_client_to_server
      name-list    encryption_algorithms_server_to_client
      name-list    mac_algorithms_client_to_server
      name-list    mac_algorithms_server_to_client
      name-list    compression_algorithms_client_to_server
      name-list    compression_algorithms_server_to_client
      name-list    languages_client_to_server
      name-list    languages_server_to_client
      boolean      first_kex_packet_follows
      uint32       0 (reserved for future extension)
    """
    message_id = MessageIDs.SSH_MSG_KEXINIT

    def __init__(
        self,
        cookie=None,
        kex_algorithms=None,
        server_host_key_algorithms=None,
        encryption_algorithms_to_server=None,
        encryption_algorithms_from_server=None,
        mac_algorithms_to_server=None,
        mac_algorithms_from_server=None,
        compression_algorithms_to_server=None,
        compression_algorithms_from_server=None,
        languages_to_server=None,
        languages_from_server=None,
            first_kex_packet_follows=None):
        super(KexInitModel, self).__init__(locals())
        self.cookie = six.b(cookie) if cookie is not None else os.urandom(16)

    def to_bytes(self):
        msg = b""
        msg += self._write_int(self.message_id)
        msg += self.cookie[:16]
        msg += self._write_list(self.kex_algorithms)
        msg += self._write_list(self.server_host_key_algorithms)
        msg += self._write_list(self.encryption_algorithms_to_server)
        msg += self._write_list(self.encryption_algorithms_from_server)
        msg += self._write_list(self.mac_algorithms_to_server)
        msg += self._write_list(self.mac_algorithms_from_server)
        msg += self._write_list(self.compression_algorithms_to_server)
        msg += self._write_list(self.compression_algorithms_from_server)
        msg += self._write_list(self.languages_to_server)
        msg += self._write_list(self.languages_from_server)
        msg += self._write_bool(self.first_kex_packet_follows)
        msg += self._write_int(0, 4)
        return msg
