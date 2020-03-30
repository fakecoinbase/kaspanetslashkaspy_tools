from kaspy_tools.utils import general_utils


class TxOut:
    """
    This object holds all required methods to handle all types of TxOuts.
    """
    def __init__(self, value_bytes=None, script_pub_key_len_bytes=0, script_pub_key_bytes=None, script_pub_key=None):
        self._value=None
        self._value_bytes = value_bytes
        self._script_pub_key_len_bytes = script_pub_key_len_bytes  # re-added
        self._script_pub_key_bytes = script_pub_key_bytes
        self._script_pub_key = script_pub_key

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_tx_out(block_bytes_stream):
        """
        Parse "tx out" data and returns as bytes array.

        :param block_bytes_stream: The bytes stream that holds the tx out data
        :return: TxOut class object
        """
        tx_out_parameters = {"value": 8, "scriptPubKeyLen": "VARINT", "SCRIPT_PUB_KEY": "scriptPubKeyLen"}
        value = block_bytes_stream.read(tx_out_parameters["value"])
        script_pub_key_len_int, script_pub_key_len_bytes = general_utils.read_varint(block_bytes_stream)
        script_pub_key = block_bytes_stream.read(script_pub_key_len_int)
        return TxOut(value, script_pub_key_len_bytes, script_pub_key)

    @classmethod
    def tx_out_factory(cls, *, value=0, script_pub_key=None):
        new_tx_out = cls()
        new_tx_out.set_value(value)
        new_tx_out.set_value_bytes(None)
        new_tx_out._script_pub_key_len = None
        new_tx_out._script_pub_key_len_bytes = None
        new_tx_out._script_pub_key = script_pub_key
        return new_tx_out



    # ========== Set Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_value(self, value):
        """ Sets variable "_value" to the received value"""
        self._value = value

    def set_value_bytes(self, value_bytes):
        """ Sets variable "_value" to the received value"""
        self._value_bytes = value_bytes


    def set_script_pub_key_len(self, script_pub_key_len):
        """ Sets variable "_script_pub_key_len" to the received value"""
        self._script_pub_key_len = script_pub_key_len


    def set_script_pub_key(self, script_pub_key):
        self._script_pub_key = script_pub_key

    def set_script_pub_key_bytes(self, script_pub_key_bytes):
        """ Sets variable "_script_pub_key" to the received value"""
        self._script_pub_key_bytes = script_pub_key_bytes
    # ========== Get Methods ========== #

    def get_value(self):
        """
        :return: value as bytes
        """
        return self._value

    def get_value_bytes(self):
        """
        :return: value as bytes
        """
        if not self._value_bytes:
            self._value_bytes = (self._value).to_bytes(8, byteorder='little')
        return self._value_bytes

    def get_script_pub_key_len(self):
        """
        :return: script_pub_key_len as bytes
        """
        return self._script_pub_key_len

    def get_script_pub_key_len_bytes(self):
        """
        :return: script_pub_key_len as bytes
        """
        if not self._script_pub_key_len_bytes:
            self._script_pub_key_len_bytes = general_utils.write_varint(self._script_pub_key_len)
        return self._script_pub_key_len_bytes


    def get_script_pub_key(self):
        """
        :return: script_pub_key as script object
        """
        return self._script_pub_key

    def get_script_pub_key_bytes(self):
        """
        :return: script_pub_key as bytes
        """
        if not self._script_pub_key_bytes:
            self._script_pub_key_bytes = bytes(self._script_pub_key)
            self._script_pub_key_len = len(self._script_pub_key_bytes)
        return self._script_pub_key_bytes


    def get_tx_out_bytes(self):
        """
        :return: Tx Out bytes as a list
        """
        tx_out_list = []
        tx_out_list.extend([[self.get_value_bytes()], [self.get_script_pub_key_len_bytes()],
                            [self.get_script_pub_key_bytes()]])
        tx_out_bytes = general_utils.flatten_nested_iterable(tx_out_list)
        return tx_out_bytes

    def __bytes__(self):
        """
        Convert this instance of tx_out to bytes, and returns the bytes object.
        :return: The bytes representation of this tx_out object
        """
        ret_bytes = b''
        ret_bytes += self.get_value_bytes()
        script_bytes = self.get_script_pub_key_bytes()
        script_len_bytes = self.get_script_pub_key_len_bytes()
        ret_bytes += script_len_bytes
        ret_bytes += script_bytes
        return ret_bytes