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

    def __init__(self, *, version_bytes=None,num_of_txs_in_bytes=0, tx_in_list=None,
                 num_of_txs_out_bytes=0, tx_out_list=None, locktime_bytes=None, subnetwork_id_bytes=None,
                 gas_bytes=None, payload_hash_bytes=None, payload_length_bytes=None, payload_bytes=None):
        self._version_bytes = version_bytes
        self._number_of_txs_in_bytes = num_of_txs_in_bytes  # re-added
        self._tx_in_list = tx_in_list
        self._number_of_txs_out_bytes = num_of_txs_out_bytes  # re-added
        self._tx_out_list = tx_out_list
        self._locktime_bytes = locktime_bytes
        self._subnetwork_id_bytes = subnetwork_id_bytes
        self._gas_bytes = gas_bytes
        self._payload_hash_bytes = payload_hash_bytes
        self._payload_length_bytes = payload_length_bytes
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
        num_of_txs_in_int, num_of_txs_in_bytes = general_utils.read_varint(block_bytes_stream)
        tx_in_list = []
        for i in range(num_of_txs_in_int):  # loops through all txs in
            tx_in = TxIn.parse_tx_in(block_bytes_stream)
            tx_in_list.append(tx_in)
        num_of_txs_out_int, num_of_txs_out_bytes = general_utils.read_varint(block_bytes_stream)
        tx_out_list = []
        for i in range(num_of_txs_out_int):  # loops through all txs out
            tx_out = TxOut.parse_tx_out(block_bytes_stream)
            tx_out_list.append(tx_out)
        locktime_bytes = block_bytes_stream.read(tx_parameters["locktime"])
        subnetwork_id_bytes = block_bytes_stream.read(tx_parameters["subnetworkID"])
        if subnetwork_id_bytes == NATIVE_SUBNETWORK_ID:
            return Tx(version_bytes=version_bytes,
                      num_of_txs_in_bytes=num_of_txs_in_bytes, tx_in_list=tx_in_list,
                      num_of_txs_out_bytes=num_of_txs_out_bytes, tx_out_list=tx_out_list,
                      locktime_bytes=locktime_bytes, subnetwork_id_bytes=subnetwork_id_bytes)
        else:
            gas_bytes = block_bytes_stream.read(tx_parameters["gas"])
            payload_hash_bytes = block_bytes_stream.read(tx_parameters["payloadHash"])
            payload_length_int, payload_length_bytes = general_utils.read_varint(block_bytes_stream)
            payload_bytes = block_bytes_stream.read(payload_length_int)
            return Tx(version_bytes=version_bytes, num_of_txs_in_bytes=num_of_txs_in_bytes, tx_in_list=tx_in_list,
                      num_of_txs_out_bytes=num_of_txs_out_bytes, tx_out_list=tx_out_list,
                      locktime_bytes=locktime_bytes, subnetwork_id_bytes=subnetwork_id_bytes,
                      gas_bytes=gas_bytes, payload_hash_bytes=payload_hash_bytes,
                      payload_length_bytes=payload_length_bytes, payload_bytes=payload_bytes)

    # ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_tx_in_list(self, tx_in_list):
        """
        add a list of tx_in objects, to current input objects
        :param tx_in_list: list with new input objects
        :return:
        """
        self._tx_in_list = tx_in_list
        self._number_of_txs_in = len(tx_in_list)


    def set_tx_out_list(self, tx_out_list):
        """
        add a list of tx_out objects, to current output objects
        :param tx_out_list:
        :return:
        """
        self._tx_out_list = tx_out_list
        self._number_of_txs_out = len(tx_out_list)

    # ========== Set Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_version_bytes(self, version_bytes):
        """ Sets variable "_version" to the received value"""
        self._version_bytes = version_bytes
   
    def set_locktime(self, lock_time):
        """ Sets variable "_locktime" to the received value"""
        self._locktime = lock_time

    def set_locktime_bytes(self, lock_time_bytes):
        """ Sets variable "_locktime" to the received value"""
        self._locktime_bytes = lock_time_bytes

    def set_subnetwork_id(self, subnetwork_id):
        """ Sets variable "_subnetwork_id" to the received value"""
        self._subnetwork_id = subnetwork_id

    # ========== Get Methods ========== #



    def get_version_bytes(self):
        """
        :return: Version as bytes
        """
        return self._version_bytes


    def get_number_of_txs_in(self):
        """
        :return: Number of txs in as bytes
        """
        return self._number_of_txs_in

    def get_tx_in_list(self):
        """
        :return: Tx in as bytes
        """
        return self._tx_in_list

    def get_number_of_txs_out(self):
        """
        :return: Number of txs out as bytes
        """
        return self._number_of_txs_out

    def get_tx_out(self):
        """
        :return: Tx out as bytes
        """
        return self._tx_out_list

    def get_locktime(self):
        """
        :return: Locktime as bytes
        """
        return self._locktime

    def get_locktime_bytes(self):
        """
        :return: Locktime as bytes
        """
        if not self._locktime_bytes:
            self._locktime_bytes = (self._locktime).to_bytes(8, byteorder='little')
        return self._locktime_bytes


    def get_subnetwork_id(self):
        """
        :return: Subnetwork ID as bytes
        """
        return self._subnetwork_id

    def get_tx_bytes(self):
        """
        :return: Tx bytes as a list
        """
        tx_list = []
        tx_list.extend([[self._version_bytes], [self._number_of_txs_in]])
        for i in self._tx_in_list:
            tx_list.append(i.get_tx_in_bytes())
        tx_list.extend([[self._number_of_txs_out]])
        for i in self._tx_out_list:
            tx_list.append(i.get_tx_out_bytes())
        tx_list.extend([[self._locktime_bytes], [self._subnetwork_id]])
        if self._subnetwork_id != NATIVE_SUBNETWORK_ID:
            tx_list.extend([[self._gas], [self._payload_hash], [self._payload_length], [self._payload]])
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

    def __bytes__(self):
        ret_bytes = b''
        ret_bytes += self.get_version_bytes()
        ret_bytes += general_utils.write_varint(self._number_of_txs_in)
        for tx_in in self._tx_in_list:
            ret_bytes += bytes(tx_in)

        ret_bytes += general_utils.write_varint(self.get_number_of_txs_out())  # the number of tx outputs
        for tx_out in self._tx_out_list:
            ret_bytes += bytes(tx_out)

        ret_bytes += self.get_locktime_bytes()  # adding locktime - already in bytes
        ret_bytes += self._subnetwork_id  # subnetwork id - 20 bytes
        # if self._subnetwork_id == NATIVE_SUBNETWORK:
        #     ret_bytes += self._gas.to_bytes(8, byteorder = 'little')    # add GAS
        #     ret_bytes += bytes.fromhex(self._payload_hash)      # add payload hash
        # TODO: payload and payload length

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
