from utils import general_utils

TX_IN_SEQUENCE = bytes(8)


class TxIn:
    """
    This object holds all required methods to handle all types of TxIns.
    """

    def __init__(self, previous_tx_id, previous_tx_out_index, next_variable_length_bytes, coinbase_or_script_sig, private_key,
                 sequence=TX_IN_SEQUENCE):
        self._previous_tx_id = previous_tx_id
        self._previous_tx_out_index = previous_tx_out_index
        self._next_variable_length = next_variable_length_bytes  # was removed by Yuval's update
        self._coinbase_or_script_sig = coinbase_or_script_sig
        self._private_key = private_key
        self._sequence = sequence

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_tx_in(block_bytes_stream):
        """
        Parse "tx in" data and returns as bytes array.

        :param block_bytes_stream: The bytes stream that holds the coinbase tx in data
        :return: TxIn class object
        """
        tx_in_parameters = {"previous_tx_id": 32, "previous_tx_out_index": 4, "next_variable_length": "VARINT",
                            "coinbase_or_script_sig": "next_variable_length", "sequence": 8}
        previous_tx_id = block_bytes_stream.read(tx_in_parameters["previous_tx_id"])
        previous_tx_out_index = block_bytes_stream.read(tx_in_parameters["previous_tx_out_index"])
        next_variable_length_int, next_variable_length_bytes = general_utils.read_varint(block_bytes_stream)
        coinbase_or_script_sig = block_bytes_stream.read(next_variable_length_int)
        sequence = block_bytes_stream.read(tx_in_parameters["sequence"])
        return TxIn(previous_tx_id, previous_tx_out_index, next_variable_length_bytes, coinbase_or_script_sig, sequence)

    # ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!
    def update_previous_tx_id(self):
        pass

    def update_previous_tx_index(self):
        pass

    def update_next_variable_length(self):
        pass

    def update_coinbase_or_script_sig(self):
        pass

    def update_sequence(self):
        pass

    # ========== Set Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_previous_tx_id(self, previous_tx_id):
        """ Sets variable "_previous_tx_id" to the received value"""
        self._previous_tx_id = previous_tx_id

    def set_previous_tx_index(self, previous_tx_index):
        """ Sets variable "_previous_tx_index" to the received value"""
        self._previous_tx_index = previous_tx_index

    def set_next_variable_length(self, next_variable_length):
        """ Sets variable "_next_variable_length" to the received value"""
        self._next_variable_length = next_variable_length

    def set_coinbase_or_script_sig(self, coinbase_or_script_sig):
        """ Sets variable "_coinbase_or_script_sig" to the received value"""
        self._coinbase_or_script_sig = coinbase_or_script_sig

    def set_sequence(self, sequence):
        """ Sets variable "_sequence" to the received value"""
        self._sequence = sequence

    # ========== Get Methods ========== #

    def get_previous_tx_id(self):
        """
        :return: previous_tx_id as bytes
        """
        return self._previous_tx_id

    def get_previous_tx_index(self):
        """
        :return: previous_tx_index as bytes
        """
        return self._previous_tx_index

    def get_next_variable_length(self):
        """
        :return: next_variable_length as bytes
        """
        return self._next_variable_length

    def get_coinbase_or_script_sig(self):
        """
        :return: coinbase_or_script_sig as bytes
        """
        return self._coinbase_or_script_sig

    def get_sequence(self):
        """
        :return: sequence as bytes
        """
        return self._sequence

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
        tx_list.extend([self._previous_tx_id, self._previous_tx_index, self._sequence])
        tx_in_bytes = general_utils.flatten_nested_iterable(tx_list)
        return tx_in_bytes

    def get_tx_in_bytes(self):
        """
        :return: Tx In bytes as a list
        """
        tx_in_list = []
        tx_in_list.extend([[self._previous_tx_id], [self._previous_tx_out_index], [self._next_variable_length],
                           [self._coinbase_or_script_sig], self._sequence])
        tx_in_bytes = general_utils.flatten_nested_iterable(tx_in_list)
        return tx_in_bytes

    def __bytes__(self):
        """
        Convert this instance of tx_in to bytes, and returns the bytes object.
        :return: The bytes representation of this tx_in object
        """
        ret_bytes = b''
        ret_bytes += bytes.fromhex(self._previous_tx_id)  # previous tx id
        ret_bytes += self._previous_tx_out_index.to_bytes(4, byteorder='little')  # prev tx output index
        # coinbase or script
        coinbase_or_script = bytes(self._coinbase_or_script_sig)  # compute coinbase or script bytes
        ret_bytes += general_utils.write_varint(len(coinbase_or_script))  # coinbase or script len (varint)
        ret_bytes += coinbase_or_script  # add coinbase or script bytes
        ret_bytes += self._sequence
        return ret_bytes
