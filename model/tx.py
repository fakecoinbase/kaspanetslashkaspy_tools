import hashlib
from utils import general_utils
from model.tx_in import TxIn
from model.tx_out import TxOut

NATIVE_SUBNETWORK_ID = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    def __init__(self, version, num_of_txs_in, tx_in_list, num_of_txs_out, tx_out_list, locktime, subnetwork_id,
                 gas=None, payload_hash=None, payload_length=None, payload=None):
        self._version = version
        self._number_of_txs_in = num_of_txs_in  # re-added
        self._tx_in_list = tx_in_list
        self._number_of_txs_out = num_of_txs_out  # re-added
        self._tx_out_list = tx_out_list
        self._locktime = locktime
        self._subnetwork_id = subnetwork_id
        self._gas = gas
        self._payload_hash = payload_hash
        self._payload_length = payload_length
        self._payload = payload

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
        version = block_bytes_stream.read(tx_parameters["version"])
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
        locktime = block_bytes_stream.read(tx_parameters["locktime"])
        subnetwork_id = block_bytes_stream.read(tx_parameters["subnetworkID"])
        if subnetwork_id == NATIVE_SUBNETWORK_ID:
            return Tx(version, num_of_txs_in_bytes, tx_in_list, num_of_txs_out_bytes, tx_out_list, locktime,
                      subnetwork_id)
        else:
            gas = block_bytes_stream.read(tx_parameters["gas"])
            payload_hash = block_bytes_stream.read(tx_parameters["payloadHash"])
            payload_length_int, payload_length_bytes = general_utils.read_varint(block_bytes_stream)
            payload = block_bytes_stream.read(payload_length_int)
            return Tx(version, num_of_txs_in_bytes, tx_in_list, num_of_txs_out_bytes, tx_out_list, locktime,
                      subnetwork_id, gas, payload_hash, payload_length_bytes, payload)

    # ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def update_version(self):
        pass

    def update_txs_in(self):
        pass

    def add_tx_in(self, new_tx_in):
        self._tx_in_list.append(new_tx_in)

    def update_txs_out(self):
        pass

    def add_tx_out(self, new_tx_out):
        self._tx_out_list.append(new_tx_out)

    def update_locktime(self):
        pass

    def update_subnetwork_id(self):
        pass

    # ========== Set Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

    def set_version(self, version):
        """ Sets variable "_version" to the received value"""
        self._version = version

    def set_number_of_txs_in(self, num_of_txs_in):
        """ Sets variable "_number_of_txs_in" to the received value"""
        self._number_of_txs_in = num_of_txs_in

    def set_tx_in(self, tx_in):
        """ Sets variable "_tx_in" to the received value"""
        self._tx_in_list = tx_in

    def set_number_of_txs_out(self, num_of_txs_out):
        """ Sets variable "_number_of_txs_out" to the received value"""
        self._number_of_txs_out = num_of_txs_out

    def set_txs_out(self, tx_out):
        """ Sets variable "_tx_out" to the received value"""
        self._tx_out_list = tx_out

    def set_locktime(self, lock_time):
        """ Sets variable "_locktime" to the received value"""
        self._locktime = lock_time

    def set_subnetwork_id(self, subnetwork_id):
        """ Sets variable "_subnetwork_id" to the received value"""
        self._subnetwork_id = subnetwork_id

    # ========== Get Methods ========== #

    def get_version(self):
        """
        :return: Version as bytes
        """
        return self._version

    def get_number_of_txs_in(self):
        """
        :return: Number of txs in as bytes
        """
        return self._number_of_txs_in

    def get_tx_in(self):
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
        tx_list.extend([[self._version], [self._number_of_txs_in]])
        for i in self._tx_in_list:
            tx_list.append(i.get_tx_in_bytes())
        tx_list.extend([[self._number_of_txs_out]])
        for i in self._tx_out_list:
            tx_list.append(i.get_tx_out_bytes())
        tx_list.extend([[self._locktime], [self._subnetwork_id]])
        if self._subnetwork_id != NATIVE_SUBNETWORK_ID:
            tx_list.extend([[self._gas], [self._payload_hash], [self._payload_length], [self._payload]])
        tx_bytes = general_utils.flatten_nested_iterable(tx_list)
        return tx_bytes

    def get_tx_bytes_for_hash_merkle_root(self):
        """
        :return: Tx bytes array in a format specifically required for calculating the hash merkle root
        """
        tx_list = []
        tx_list.extend([[self._version], [self._number_of_txs_in]])
        for i in self._tx_in_list:
            tx_list.append(i.get_tx_in_bytes())
        tx_list.extend([[self._number_of_txs_out]])
        for i in self._tx_out_list:
            tx_list.append(i.get_tx_out_bytes())
        tx_list.extend([[self._locktime], [self._subnetwork_id]])
        if self._subnetwork_id != NATIVE_SUBNETWORK_ID:
            tx_list.extend([[self._gas], [self._payload_hash], [b"\x00"]])
        tx_bytes = general_utils.build_element_from_list(tx_list)
        return tx_bytes

    def __bytes__(self):
        ret_bytes = b''
        ret_bytes += self._version
        ret_bytes += general_utils.write_varint(self._number_of_txs_in)
        for tx_in in self._tx_in_list:
            ret_bytes += bytes(tx_in)

        ret_bytes += general_utils.write_varint(self.get_number_of_txs_out())  # the number of tx outputs
        for tx_out in self._tx_out_list:
            ret_bytes += bytes(tx_out)

        ret_bytes += self._locktime  # adding locktime - already in bytes
        ret_bytes += self._subnetwork_id  # subnetwork id - 20 bytes
        # if self._subnetwork_id == NATIVE_SUBNETWORK:
        #     ret_bytes += self._gas.to_bytes(8, byteorder = 'little')    # add GAS
        #     ret_bytes += bytes.fromhex(self._payload_hash)      # add payload hash
        # TODO: payload and payload length

        return ret_bytes

    def compute_txid(self, store=False, in_hex=True):
        """
        compute_txid computes the transaction id by hashing it twice (sha256).
        It tries to use the binary representation of the transaction if it was already computed.
        If there is no binary tx representation, compute_txid raises a ValueError.
        :param store: Set to True if you want the txid to also be stored (in bytes form)
        :param in_hex: Est to True if you want to receive the result in hexadecimal.
        :return: The txid of the transaction.
        """
        if self._tx_bytes is not None:
            m1 = hashlib.sha256()
            m2 = hashlib.sha256()
            sha256_once = m1.update(self._tx_bytes).digest()
            sha256_twice = m2.update(sha256_once).digest()
            if store == True:
                self._tdid = sha256_twice
            if in_hex == True:
                return sha256_twice.hex()
            else:
                return sha256_twice
        else:
            raise ValueError
