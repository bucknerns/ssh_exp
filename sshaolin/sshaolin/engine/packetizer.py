

    def send_message(self, data):
        """
        Write a block of data using the current cipher, as an SSH block.
        """
        # encrypt this sucka
        data = asbytes(data)
        cmd = byte_ord(data[0])
        if cmd in MSG_NAMES:
            cmd_name = MSG_NAMES[cmd]
        else:
            cmd_name = '$%x' % cmd
        orig_len = len(data)
        self.__write_lock.acquire()
        try:
            if self.__compress_engine_out is not None:
                data = self.__compress_engine_out(data)
            packet = self._build_packet(data)
            if self.__dump_packets:
                self._log(DEBUG, 'Write packet <%s>, length %d' % (cmd_name, orig_len))
                self._log(DEBUG, util.format_binary(packet, 'OUT: '))
            if self.__block_engine_out is not None:
                out = self.__block_engine_out.update(packet)
            else:
                out = packet
            # + mac
            if self.__block_engine_out is not None:
                payload = struct.pack('>I', self.__sequence_number_out) + packet
                out += compute_hmac(self.__mac_key_out, payload, self.__mac_engine_out)[:self.__mac_size_out]
            self.__sequence_number_out = (self.__sequence_number_out + 1) & xffffffff
            self.write_all(out)

            self.__sent_bytes += len(out)
            self.__sent_packets += 1
            if (self.__sent_packets >= self.REKEY_PACKETS or self.__sent_bytes >= self.REKEY_BYTES)\
                    and not self.__need_rekey:
                # only ask once for rekeying
                self._log(DEBUG, 'Rekeying (hit %d packets, %d bytes sent)' %
                          (self.__sent_packets, self.__sent_bytes))
                self.__received_bytes_overflow = 0
                self.__received_packets_overflow = 0
                self._trigger_rekey()
        finally:
            self.__write_lock.release()
