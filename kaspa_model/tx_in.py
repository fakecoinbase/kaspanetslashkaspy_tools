from kaspy_tools.utils import general_utils

NATIVE_SUBNETWORK_ID = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # re-added
TX_IN_SEQUENCE = bytes(8)


class TxIn:
    """
    This object holds all required methods to handle all types of TxIns.
    """

    def __init__(self, previous_tx_id_bytes=None, previous_tx_out_index_bytes=None, next_variable_length=0,
                 coinbase_or_script_sig=None,
                 sequence_bytes=None, private_key=None):
        self._previous_tx_id_bytes = previous_tx_id_bytes
        self._previous_tx_out_index_bytes = previous_tx_out_index_bytes  # re-named to previous_tx_index
        self._next_variable_length = next_variable_length  # re-added
        self._coinbase_or_script_sig = coinbase_or_script_sig
        self._sequence_bytes = sequence_bytes
        self._private_key = private_key  # changed position to last

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_tx_in(block_bytes_stream):
        """
        Parse "tx in" data and returns as bytes array.

        :param block_bytes_stream: The bytes stream that holds the coinbase tx in data
        :return: TxIn class object
        """
        tx_in_parameters = {"previous_tx_id_bytes": 32, "previous_tx_index": 4, "next_variable_length": "VARINT",
                            "coinbase_or_script_sig": "next_variable_length", "sequence": 8}
        previous_tx_id = block_bytes_stream.read(tx_in_parameters["previous_tx_id_bytes"])
        previous_tx_index = block_bytes_stream.read(tx_in_parameters["previous_tx_index"])
        next_variable_length_int, next_variable_length_bytes = general_utils.read_varint(block_bytes_stream)
        coinbase_or_script_sig = block_bytes_stream.read(next_variable_length_int)
        sequence = block_bytes_stream.read(tx_in_parameters["sequence"])
        return TxIn(previous_tx_id, previous_tx_index, next_variable_length_bytes, coinbase_or_script_sig, sequence)

    @classmethod
    def tx_in_factory(cls, *, previous_tx_id=None, previous_tx_out_index=None, script=None,
                      sequence=None, private_key=None):
        new_tx_in = cls()

        new_tx_in.set_previous_tx_id(previous_tx_id)
        new_tx_in.set_previous_tx_id_bytes(None)
        new_tx_in.set_previous_tx_out_index(previous_tx_out_index)
        new_tx_in.set_previous_tx_out_index_bytes(None)

        new_tx_in.set_script(script)
        new_tx_in.set_sequence(sequence)
        new_tx_in.set_sequence_bytes(None)
        new_tx_in.set_private_key(private_key)
        return new_tx_in

    # ========== Set Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_previous_tx_id(self, previous_tx_id):
        """ Sets variable "_previous_tx_id" to the received value"""
        self._previous_tx_id = previous_tx_id

    def set_previous_tx_id_bytes(self, previous_tx_id_bytes):
        self._previous_tx_id_bytes = previous_tx_id_bytes

    def set_previous_tx_out_index(self, previous_tx_out_index):
        """ Sets variable "_previous_tx_index" to the received value"""
        self._previous_tx_out_index = previous_tx_out_index

    def set_previous_tx_out_index_bytes(self, previous_tx_out_index_bytes):
        """ Sets variable "_previous_tx_index" to the received value"""
        self._previous_tx_out_index_bytes = previous_tx_out_index_bytes

    def set_next_variable_length(self, next_variable_length):
        """ Sets variable "_next_variable_length" to the received value"""
        self._next_variable_length = next_variable_length

    def set_coinbase_or_script_sig(self, coinbase_or_script_sig):
        """ Sets variable "_coinbase_or_script_sig" to the received value"""
        self._coinbase_or_script_sig = coinbase_or_script_sig

    def set_sequence(self, sequence):
        """ Sets variable "_sequence" to the received value"""
        self._sequence = sequence

    def set_sequence_bytes(self, sequence_bytes):
        """ Sets variable "_sequence" to the received value"""
        self._sequence_bytes = sequence_bytes

    def set_script(self, script):
        self._script = script

    def set_private_key(self, private_key):
        self._private_key = private_key

    # ========== Get Methods ========== #

    def get_previous_tx_id(self):
        """
        :return: previous_tx_id_bytes as bytes
        """
        return self._previous_tx_id

    def get_previous_tx_id_bytes(self):
        """
        :return: previous_tx_id_bytes as bytes
        """
        if not self._previous_tx_id_bytes:
            self._previous_tx_id_bytes = bytes.fromhex(self._previous_tx_id)
        return self._previous_tx_id_bytes

    def get_previous_tx_out_index(self):
        """
        :return: previous_tx_index as bytes
        """
        return self._previous_tx_out_index

    def get_previous_tx_out_index_bytes(self):
        """
        :return: previous_tx_index as bytes
        """
        if not self._previous_tx_out_index_bytes:
            self._previous_tx_out_index_bytes = (not self._previous_tx_out_index).to_bytes(4, byteorder='little')
        return self._previous_tx_out_index_bytes

    def get_next_variable_length(self):
        """
        :return: next_variable_length as bytes
        """
        return self._next_variable_length

    def get_script(self):
        """
        :return: coinbase_or_script_sig as bytes
        """
        return self._script

    def get_sequence(self):
        """
        :return: sequence as bytes
        """
        return self._sequence

    def get_sequence_bytes(self):
        """
        Lazily set self._sequence_bytes, and returns it
        :return: sequence as bytes
        """
        if not self._sequence_bytes:
            self._sequence_bytes = (self._sequence).to_bytes(8, byteorder='little')
        return self._sequence_bytes

    def get_private_key(self):
        """
        Returns the private key that this input uses
        :return: the stored private key
        """
        return self._private_key

    def get_tx_in_bytes_for_previous_tx_id(self):
        """
        :return: TxIn bytes array in a format specifically required for calculating the previous tx ID
        """
        tx_list = []
        tx_list.extend([self._previous_tx_id, self._previous_tx_out_index, self._sequence])
        tx_in_bytes = general_utils.flatten_nested_iterable(tx_list)
        return tx_in_bytes

    def get_tx_in_bytes(self):
        """
        :return: Tx In bytes as a list
        """
        tx_in_list = []
        tx_in_list.extend(
            [[self.get_previous_tx_id_bytes()], [self.get_previous_tx_out_index_bytes()], [self._next_variable_length],
             [self._coinbase_or_script_sig], self._sequence_bytes])
        tx_in_bytes = general_utils.flatten_nested_iterable(tx_in_list)
        return tx_in_bytes

    def __bytes__(self):
        """
        Convert this instance of tx_in to bytes, and returns the bytes object.
        :return: The bytes representation of this tx_in object
        """
        ret_bytes = b''
        ret_bytes += self.get_previous_tx_id_bytes()[::-1]  # should reverse the order of bytes
        ret_bytes += self.get_previous_tx_out_index_bytes()
        # coinbase or script
        script_bytes = bytes(self.get_script())  # compute coinbase or script bytes
        ret_bytes += general_utils.write_varint(len(script_bytes))  # coinbase or script len (varint)
        ret_bytes += script_bytes  # add coinbase or script bytes
        ret_bytes += self.get_sequence_bytes()
        return ret_bytes
