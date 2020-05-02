import hashlib
from kaspy_tools.logs import config_logger
from kaspy_tools.utils import general_utils
from kaspy_tools.kaspa_model.tx_in import TxIn
from kaspy_tools.kaspa_model.tx_out import TxOut

KT_logger = config_logger.get_kaspy_tools_logger()

NATIVE_SUBNETWORK_ID = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
COINBASE_SUBNETWORK = ''.join(['00' for i in range(19)]) + '01'
CURRENT_VERSION = b'\x01\x00\x00\x00'
NATIVE_SUBNETWORK = b'\x00' * 20  # native subnetwork is 20 zero bytes
VERSION_1 = (1).to_bytes(4, byteorder='little')  # convert int to 32 bites little endian
LOCKTIME_NO_LOCK = bytes(8)


class Tx:
    """
    This object holds all required methods to handle all types of Txs.
        :param version:
        :param num_of_txs_in:  (int) the number of tx inputs
        :param tx_in_list:  A list of inputs (e.g: [('---tx--hash---', output-number, 'script-sig'), (....),...]  )
    """

    def __init__(self, *, version_bytes=None, number_of_tx_inputs_bytes=0, tx_input_list=None,
                 number_of_tx_outputs_bytes=0, tx_output_list=None, locktime_bytes=None, subnetwork_id_bytes=None,
                 gas_bytes=None, payload_hash_bytes=None, payload_length_bytes=None, payload_bytes=None):
        self._version_bytes = version_bytes
        self._number_of_tx_inputs_bytes = number_of_tx_inputs_bytes
        self._number_of_tx_inputs_int = None
        self._tx_input_list = tx_input_list
        self._number_of_tx_outputs_bytes = number_of_tx_outputs_bytes
        self._number_of_tx_outputs_int = None
        self._tx_output_list = tx_output_list
        self._locktime_bytes = locktime_bytes
        self._locktime_int = None
        self._subnetwork_id_bytes = subnetwork_id_bytes
        self._gas_bytes = gas_bytes
        self._payload_hash_bytes = payload_hash_bytes
        self._payload_length_bytes = payload_length_bytes
        self._payload_length_int = None
        self._payload_bytes = payload_bytes

    @classmethod
    def tx_factory(cls, *, version_bytes=None, tx_in_list=None, tx_out_list=None, locktime=None, subnetwork_id=None,
                   gas=None, payload_hash=None, payload=None):
        new_tx = cls()
        new_tx.set_version_bytes(version_bytes)
        new_tx.set_tx_in_list(tx_in_list)
        new_tx.set_tx_out_list(tx_out_list)
        new_tx.set_locktime(locktime)
        new_tx.set_locktime_bytes(None)
        new_tx.set_subnetwork_id(subnetwork_id)
        new_tx._gas = gas
        new_tx._payload_hash = payload_hash
        new_tx._payload = payload
        return new_tx

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_tx(block_bytes_stream):
        """
        Parse a "Tx" either it's coinbase or native and returns a Tx class object.

        :param block_bytes_stream: The bytes stream that holds the coinbase tx in data
        :return: Tx class object
        """
        tx_parameters = {"version": 4, "numTxIns": "VARINT", "TX_IN": "TX_IN x numTuxIns",
                         "numTxOut": "VARINT", "TX_OUT": "TX_OUT x numTxOuts", "locktime": 8, "subnetworkID": 20,
                         "gas": 8, "payloadHash": 32, "payloadLength": "VARINT", "payload": "payloadLength"}
        version_bytes = block_bytes_stream.read(tx_parameters["version"])
        number_of_txs_inputs_int, number_of_txs_inputs_bytes = general_utils.read_varint(block_bytes_stream)
        tx_input_list = []
        for i in range(number_of_txs_inputs_int):  # loops through all txs in
            tx_in = TxIn.parse_tx_in(block_bytes_stream)
            tx_input_list.append(tx_in)
        _number_of_tx_outputs_int, number_of_tx_outputs_bytes = general_utils.read_varint(block_bytes_stream)
        tx_output_list = []
        for i in range(_number_of_tx_outputs_int):  # loops through all txs out
            tx_out = TxOut.parse_tx_out(block_bytes_stream)
            tx_output_list.append(tx_out)
        locktime_bytes = block_bytes_stream.read(tx_parameters["locktime"])
        subnetwork_id_bytes = block_bytes_stream.read(tx_parameters["subnetworkID"])
        if subnetwork_id_bytes == NATIVE_SUBNETWORK_ID:
            return Tx(version_bytes=version_bytes,
                      number_of_tx_inputs_bytes=number_of_txs_inputs_bytes, tx_input_list=tx_input_list,
                      number_of_tx_outputs_bytes=number_of_tx_outputs_bytes, tx_output_list=tx_output_list,
                      locktime_bytes=locktime_bytes, subnetwork_id_bytes=subnetwork_id_bytes)
        else:
            gas_bytes = block_bytes_stream.read(tx_parameters["gas"])
            payload_hash_bytes = block_bytes_stream.read(tx_parameters["payloadHash"])
            payload_length_int, payload_length_bytes = general_utils.read_varint(block_bytes_stream)
            payload_bytes = block_bytes_stream.read(payload_length_int)
            return Tx(version_bytes=version_bytes,
                      number_of_tx_inputs_bytes=number_of_txs_inputs_bytes, tx_input_list=tx_input_list,
                      number_of_tx_outputs_bytes=number_of_tx_outputs_bytes, tx_output_list=tx_output_list,
                      locktime_bytes=locktime_bytes, subnetwork_id_bytes=subnetwork_id_bytes,
                      gas_bytes=gas_bytes, payload_hash_bytes=payload_hash_bytes,
                      payload_length_bytes=payload_length_bytes, payload_bytes=payload_bytes)

    # ========== Get properties ========== #

    @property
    def version_bytes(self):
        """
        :return: Version as bytes
        """
        return self._version_bytes

    @property
    def number_of_tx_inputs_bytes(self):
        """
        :return: Number of txs in as bytes
        """
        if (self._number_of_tx_inputs_bytes == None) and (self._number_of_tx_inputs_int != None):
            self._number_of_tx_inputs_bytes = general_utils.write_varint(self._number_of_tx_inputs_int)

        return self._number_of_tx_inputs_bytes

    @property
    def number_of_tx_inputs_int(self):
        """
        :return: Number of txs in as bytes
        """
        return self._number_of_tx_inputs_int

    @property
    def tx_input_list(self):
        """
        :return: List of TxIn objects
        """
        return self._tx_input_list

    @property
    def number_of_tx_outputs_bytes(self):
        """
        :return: Number of txs out as bytes
        """
        if (self._number_of_tx_outputs_bytes == None) and (self._number_of_tx_outputs_int != None):
            self._number_of_tx_outputs_bytes = general_utils.write_varint(self._number_of_tx_outputs_int)

        return self._number_of_tx_outputs_bytes

    @property
    def number_of_tx_outputs_int(self):
        """
        :return: Number of txs out as bytes
        """
        return self._number_of_tx_outputs_int

    @property
    def tx_output_list(self):
        """
        :return: List of TxOut objects
        """
        return self._tx_output_list

    @property
    def locktime_bytes(self):
        """
        :return: Locktime as bytes
        """
        if (self._locktime_bytes == None) and (self._locktime_int != None):
            self._locktime_bytes = (self._locktime_int).to_bytes(8, byteorder='little')
        return self._locktime_bytes

    @property
    def locktime_int(self):
        """
        :return: Locktime as bytes
        """
        return self._locktime_int

    @property
    def subnetwork_id_bytes(self):
        """
        :return: Subnetwork ID as bytes
        """
        return self._subnetwork_id_bytes

    @property
    def gas_bytes(self):
        return self._gas_bytes

    @property
    def payload_hash_bytes(self):
        return self._payload_hash_bytes

    @property
    def payload_length_bytes(self):
        return self._payload_length_bytes

    @property
    def payload_length_int(self):
        if (self._payload_length_int == None) and (self._payload_length_bytes != None):
            self._payload_length_int = int.from_bytes(self._payload_length_bytes, byteorder='little')
        return self._payload_length_int

    @property
    def payload_bytes(self):
        return self._payload_bytes

    # ========== Set Tx properties ========== #

    @version_bytes.setter
    def version_bytes(self, version_bytes):
        """ Sets variable "_version_bytes" to the received value"""
        self._version_bytes = version_bytes


    @tx_input_list.setter
    def tx_input_list(self, tx_input_list):
        """
        add a list of tx_in objects, to current input objects
        :param tx_in_list: list with new input objects
        :return:
        """
        self._tx_input_list = tx_input_list

    @tx_output_list.setter
    def tx_output_list(self, tx_output_list):
        """
        add a list of tx_out objects, to current output objects
        :param tx_out_list:
        :return:
        """
        self._tx_output_list = tx_output_list


    @locktime_int.setter
    def locktime_int(self, locktime_int):
        """ Sets variable "_locktime" to the received value"""
        self._locktime_int = locktime_int


# ******** Serialization functions **********

    def get_tx_bytes(self):
        """
        :return: Tx bytes as a list
        """
        tx_list = []
        tx_list.extend([[self.version_bytes], [self.number_of_tx_inputs_bytes]])
        for input in self._tx_input_list:
            tx_list.append(bytes(input))
        tx_list.extend([[self.number_of_tx_outputs_bytes]])
        for output in self._tx_output_list:
            tx_list.append(bytes(output))
        tx_list.extend([[self._locktime_bytes], [self.subnetwork_id_bytes]])
        if self.subnetwork_id_bytes != NATIVE_SUBNETWORK_ID:
            tx_list.extend([[self.gas_bytes], [self.payload_hash_bytes], [self.payload_length_bytes], [self.payload_bytes]])
        tx_bytes = general_utils.flatten_nested_iterable(tx_list)
        return tx_bytes

    # def get_tx_bytes_for_hash_merkle_root(self):
    #     """
    #     :return: Tx bytes array in a format specifically required for calculating the hash merkle root
    #     """
    #     tx_list = []
    #     tx_list.extend([[self._version_bytes], [self._number_of_txs_in]])
    #     for i in self._tx_in_list:
    #         tx_list.append(i.get_tx_in_bytes())
    #     tx_list.extend([[self._number_of_txs_out]])
    #     for i in self._tx_out_list:
    #         tx_list.append(i.get_tx_out_bytes())
    #     tx_list.extend([[self.get_locktime_bytes()], [self._subnetwork_id]])
    #     if self._subnetwork_id != NATIVE_SUBNETWORK_ID:
    #         tx_list.extend([[self._gas], [self._payload_hash], [b"\x00"]])
    #     tx_bytes = general_utils.build_element_from_list(tx_list)
    #     return tx_bytes

    # def get_tx_bytes_for_hash_merkle_root(self):
    #     """
    #     :return: Tx bytes array in a format specifically required for calculating the hash merkle root
    #     """
    #     tx_bytes = b''
    #     tx_bytes += self._version_bytes
    #     tx_bytes += self._number_of_txs_in
    #     for i in self._tx_in_list:
    #         tx_bytes +=  bytes(i)
    #     tx_bytes += self._number_of_txs_out
    #     for i in self._tx_out_list:
    #         tx_bytes += bytes(i)
    #     tx_bytes += self.get_locktime_bytes()
    #     tx_bytes += self._subnetwork_id
    #
    #     if self._subnetwork_id != NATIVE_SUBNETWORK_ID:
    #         tx_bytes += self._gas + self._payload_hash + b'\x00'
    #     return tx_bytes

    def get_tx_bytes_for_hash_merkle_root(self):
        ret_bytes = b''
        ret_bytes += self.version_bytes
        ret_bytes += self.number_of_tx_inputs_bytes     # computed if needed
        for tx_in in self.tx_input_list:
            ret_bytes += bytes(tx_in)

        ret_bytes += self.number_of_tx_outputs_bytes     # computed if needed
        for tx_out in self.tx_output_list:
            ret_bytes += bytes(tx_out)

        ret_bytes += self.locktime_bytes
        ret_bytes += self.subnetwork_id_bytes
        if self.subnetwork_id_bytes != NATIVE_SUBNETWORK:
            ret_bytes += self.gas_bytes
            ret_bytes += self.payload_hash_bytes
            ret_bytes += b'\x00'

        return ret_bytes

    def __bytes__(self):
        ret_bytes = b''
        ret_bytes += self.version_bytes
        ret_bytes += self.number_of_tx_inputs_bytes     # computed if needed
        for tx_in in self.tx_input_list:
            ret_bytes += bytes(tx_in)

        ret_bytes += self.number_of_tx_outputs_bytes     # computed if needed
        for tx_out in self.tx_output_list:
            ret_bytes += bytes(tx_out)

        ret_bytes += self.locktime_bytes
        ret_bytes += self.subnetwork_id_bytes
        if self.subnetwork_id_bytes == NATIVE_SUBNETWORK:
            ret_bytes += self.gas_bytes
            ret_bytes += self.payload_hash_bytes
            ret_bytes += self.payload_length_bytes
            ret_bytes += self.payload_bytes

        return ret_bytes

    # def compute_txid(self, store=False, in_hex=True):
    #     """
    #     compute_txid computes the transaction id by hashing it twice (sha256).
    #     It tries to use the binary representation of the transaction if it was already computed.
    #     If there is no binary tx representation, compute_txid raises a ValueError.
    #     :param store: Set to True if you want the txid to also be stored (in bytes form)
    #     :param in_hex: Est to True if you want to receive the result in hexadecimal.
    #     :return: The txid of the transaction.
    #     """
    #     if self._tx_bytes is not None:
    #         m1 = hashlib.sha256()
    #         m2 = hashlib.sha256()
    #         sha256_once = m1.update(self._tx_bytes).digest()
    #         sha256_twice = m2.update(sha256_once).digest()
    #         if store == True:
    #             self._tdid = sha256_twice
    #         if in_hex == True:
    #             return sha256_twice.hex()
    #         else:
    #             return sha256_twice
    #     else:
    #         raise ValueError
