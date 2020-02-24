from utils import general_utils


class TxOut:
    """
    This object holds all required methods to handle all types of TxOuts.
    """
    def __init__(self, value, script_pub_key_len, script_pub_key=None):
        self._value = value
        self._script_pub_key_len = script_pub_key_len  # re-added
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

    # ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!
    def update_value(self):
        pass

    def update_script_pub_key_len(self):
        pass

    def update_script_pub_key(self):
        pass

    # ========== Set Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_value(self, value):
        """ Sets variable "_value" to the received value"""
        self._value = value

    def set_script_pub_key_len(self, script_pub_key_len):
        """ Sets variable "_script_pub_key_len" to the received value"""
        self._script_pub_key_len = script_pub_key_len

    def set_script_pub_key(self, script_pub_key):
        """ Sets variable "_script_pub_key" to the received value"""
        self._script_pub_key = script_pub_key

    # ========== Get Methods ========== #

    def get_value(self):
        """
        :return: value as bytes
        """
        return self._value

    def get_script_pub_key_len_int(self):
        """
        :return: script_pub_key_len as bytes
        """
        return self._script_pub_key_len

    def get_script_pub_key(self):
        """
        :return: script_pub_key as bytes
        """
        return self._script_pub_key

    def get_tx_out_bytes(self):
        """
        :return: Tx Out bytes as a list
        """
        tx_out_list = []
        tx_out_list.extend([[self._value], [self._script_pub_key_len], [self._script_pub_key]])
        tx_out_bytes = general_utils.flatten_nested_iterable(tx_out_list)
        return tx_out_bytes

    def __bytes__(self):
        """
        Convert this instance of tx_out to bytes, and returns the bytes object.
        :return: The bytes representation of this tx_out object
        """
        ret_bytes = b''
        ret_bytes += (self._value).to_bytes(8, byteorder='little')    # in Satoshis
        script_bytes = bytes(self._script_pub_key)
        script_len = len(script_bytes)
        ret_bytes += general_utils.write_varint(script_len)
        ret_bytes += script_bytes
        return ret_bytes