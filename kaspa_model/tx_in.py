from kaspy_tools.logs import config_logger
from kaspy_tools.utils import general_utils
from kaspy_tools.kaspa_model.tx_script import TxScript

KT_logger = config_logger.get_kaspy_tools_logger()

NATIVE_SUBNETWORK_ID = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # re-added
TX_IN_SEQUENCE = bytes(8)


class TxIn:
    """
    This object holds all required methods to handle all types of TxIns.
    At times, we should keep several TxScript objects here:
    - a referenced script_pub_key from a referenced output object.
    - an empty script (also needed for the signing
    """

    def __init__(self, previous_tx_id_bytes=None, previous_tx_out_index_bytes=None, sig_script_length_bytes=0,
                 sig_scipt_obj=None, sequence_bytes=None, private_key=None):
        """
        Constructor for a TxIn object. All values are in bytes.
        :param previous_tx_id_bytes: The hash Id of a previous tx.
        :param previous_tx_out_index_bytes: The output index in the previous tx.
        :param next_variable_length:  Should be removed after parsing refactoring
        :param coinbase_or_script_sig: Should refactor
        :param sequence_bytes: The sequence parameter
        :param private_key:  The private key that this input "knows"
        """
        self._previous_tx_id_bytes = previous_tx_id_bytes
        self._previous_tx_out_index_bytes = previous_tx_out_index_bytes  # re-named to previous_tx_index
        self._sig_script_length_bytes = sig_script_length_bytes  # re-added
        self._sig_script = sig_scipt_obj
        self._sequence_bytes = sequence_bytes
        self._private_key = private_key  # changed position to last
        self._signed_script = None      # this is here because it is needed during signature process
        self._empty_script = None       # this is here because it is needed during signature process
        self._script_pub_key = None     # this is here because it is needed during signature process

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_tx_in(block_bytes_stream):
        """
        Parse "tx in" bytes and returns a TxIn object.
        :param block_bytes_stream: The bytes stream that holds the tx in to parse.
        :return: TxIn object
        """
        tx_in_parameters = {"previous_tx_id_bytes": 32, "previous_tx_index": 4, "next_variable_length": "VARINT",
                            "coinbase_or_script_sig": "next_variable_length", "sequence": 8}
        previous_tx_id_bytes = block_bytes_stream.read(tx_in_parameters["previous_tx_id_bytes"])
        previous_tx_out_index_bytes = block_bytes_stream.read(tx_in_parameters["previous_tx_index"])
        sig_script_length_int, sig_script_length_bytes = general_utils.read_varint(block_bytes_stream)
        sig_scipt_obj = TxScript.parse_tx_script(raw_script=block_bytes_stream, length=sig_script_length_int)

        sequence_bytes = block_bytes_stream.read(tx_in_parameters["sequence"])
        new_TxIn = TxIn(previous_tx_id_bytes=previous_tx_id_bytes, previous_tx_out_index_bytes=previous_tx_out_index_bytes,
                    sig_script_length_bytes=sig_script_length_bytes, sig_scipt_obj=sig_scipt_obj,
                    sequence_bytes=sequence_bytes)
        return new_TxIn


    @classmethod
    def tx_in_factory(cls, *, previous_tx_id=None, previous_tx_out_index=None, script=None,
                      script_pub_key=None, empty_script=None, sequence=None, private_key=None):
        """
        Creates a new TxIn object. Holds bytes values and "logical" values (like int).
        Later 'get' functions create bytes values lazily.
        :param previous_tx_id:  Previous tx id (hex str)
        :param previous_tx_out_index: Previous out index (int)
        :param script:  The sig_script (TxScript object)
        :param script_pub_key:  The referenced script_pub_key(TxScript object)
        :param empty_script:  An "empty" script (TxScript object)
        :param sequence: The sequence value (int)
        :param private_key: The 32 bytes private key (bytes)
        :return: The new TxIn object
        """
        new_tx_in = cls()

        new_tx_in.previous_tx_id(previous_tx_id)
        new_tx_in.previous_tx_id_bytes = None
        new_tx_in.previous_tx_out_index = previous_tx_out_index
        new_tx_in.previous_tx_out_index_bytes = None

        new_tx_in.sig_script = script
        new_tx_in.script_pub_key = script_pub_key
        new_tx_in.empty_script = empty_script
        new_tx_in.sequence_bytes = None
        new_tx_in.private_key = private_key
        return new_tx_in

    # ========== Get Tx Methods ========== #

    @property
    def previous_tx_id(self):
        """ Gets variable "_previous_tx_id" to the received value"""
        return self._previous_tx_id

    @property
    def previous_tx_id_bytes(self):
        if (self._previous_tx_id_bytes == None) and (self._previous_tx_id != None):
            self._previous_tx_id_bytes = bytes.fromhex(self._previous_tx_id)
        return self._previous_tx_id_bytes

    @property
    def previous_tx_out_index(self):
        return self._previous_tx_out_index

    @property
    def previous_tx_out_index_bytes(self):
        if (self._previous_tx_out_index_bytes == None) and (self._previous_tx_out_index != None):
            self._previous_tx_out_index_bytes = (self._previous_tx_out_index).to_bytes(4, byteorder='little')
        return self._previous_tx_out_index_bytes

    @property
    def sequence_bytes(self):
        return self._sequence_bytes


    @property
    def sig_script(self):
        return self._sig_script

    @property
    def private_key(self):
        return self._private_key

    @property
    def empty_script(self):
        return self._empty_script

    @property
    def script_pub_key(self):
        return self._script_pub_key

    @property
    def signed_script(self):
        return self._signed_script

    # ========== Get Methods ========== #

    @previous_tx_id.setter
    def previous_tx_id(self, previous_tx_id):
        self._previous_tx_id = previous_tx_id

    @previous_tx_id_bytes.setter
    def previous_tx_id_bytes(self, previous_tx_id_bytes):
        self._previous_tx_id_bytes = previous_tx_id_bytes

    @previous_tx_out_index.setter
    def previous_tx_out_index(self, previous_tx_out_index):
        self._previous_tx_out_index = previous_tx_out_index

    @previous_tx_out_index_bytes.setter
    def previous_tx_out_index_bytes(self, previous_tx_out_index_bytes):
        self._previous_tx_out_index_bytes = previous_tx_out_index_bytes


    @script_pub_key.setter
    def script_pub_key(self, script_pub_key):
        self._script_pub_key = script_pub_key

    @empty_script.setter
    def empty_script(self, empty_script):
        self._empty_script = empty_script

    @signed_script.setter
    def signed_script(self, signed_script):
        self._signed_script = signed_script

    @sig_script.setter
    def sig_script(self, sig_script):
        self._sig_script = sig_script

    @sequence_bytes.setter
    def sequence_bytes(self, sequence_bytes):
        self._sequence = sequence_bytes


    @private_key.setter
    def private_key(self, private_key):
        self._private_key = private_key

    def get_tx_in_bytes_for_previous_tx_id(self):
        """
        :return: TxIn bytes array in a format specifically required for calculating the previous tx ID
        """
        tx_list = []
        tx_list.extend([self._previous_tx_id, self._previous_tx_out_index, self._sequence])
        tx_in_bytes = general_utils.flatten_nested_iterable(tx_list)
        return tx_in_bytes

    # def get_tx_in_bytes(self):
    #     """
    #     :return: Tx In bytes as a list
    #     """
    #     tx_in_list = []
    #     tx_in_list.extend(
    #         [[self.get_previous_tx_id_bytes()], [self.get_previous_tx_out_index_bytes()], [self._next_variable_length],
    #          [self._coinbase_or_script_sig], self._sequence_bytes])
    #     tx_in_bytes = general_utils.flatten_nested_iterable(tx_in_list)
    #     return tx_in_bytes

    def __bytes__(self):
        """
        Convert this instance of tx_in to bytes, and returns the bytes object.
        :return: The bytes representation of this tx_in object
        """
        ret_bytes = b''
        tx_id_bytes = self.previous_tx_id_bytes[::-1]
        transposed_bytes = tx_id_bytes
        ret_bytes += transposed_bytes
        ret_bytes += self.previous_tx_out_index_bytes
        # coinbase or script
        script_bytes = bytes(self.sig_script)  # compute coinbase or script bytes
        ret_bytes += general_utils.write_varint(len(script_bytes))  # coinbase or script len (varint)
        ret_bytes += script_bytes  # add coinbase or script bytes
        ret_bytes += self.sequence_bytes
        return ret_bytes
