
from utils import general_utils

native_subnetwork_id = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class Tx:
    """
    This object holds all required methods to handle all types of Txs.
    """
    def __init__(self, version, num_of_txs_in, tx_in, num_of_txs_out, tx_out, locktime, subnetwork_id,
                 gas=None, payload_hash=None, payload_length=None, payload=None):
        self._version = version
        self._number_of_txs_in = num_of_txs_in
        self._tx_in = tx_in
        self._number_of_txs_out = num_of_txs_out
        self._tx_out = tx_out
        self._locktime = locktime
        self._subnetwork_id = subnetwork_id
        self._gas = gas
        self._payload_hash = payload_hash
        self._payload_length = payload_length
        self._payload = payload

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_tx(block_bytes_stream, tx_type=None):
        """
        Parse a "Tx" either it's coinbase or native and returns a Tx class object.

        :param block_bytes_stream: The bytes stream that holds the coinbase tx in data
        :param tx_type: Should be "coinbase" or leave empty
        :return: Tx class object
        """
        tx_parameters = {"version": 4, "numTxIns": "VARINT", "TX_IN": "TX_IN x numTuxIns",
                         "numTxOut": "VARINT", "TX_OUT": "TX_OUT x numTxOuts", "locktime": 8, "subnetworkID": 20,
                         "gas": 8, "payloadHash": 32, "payloadLength": "VARINT", "payload": "payloadLength"}
        version = block_bytes_stream.read(tx_parameters["version"])
        num_of_txs_in_int, num_of_txs_in_bytes = general_utils.read_varint(block_bytes_stream)
        tx_in_list = []
        for i in range(num_of_txs_in_int):  # loops through all txs in
            if tx_type.lower() != "coinbase" or None:
                print("Incorrect Tx_Type entered: " + str(tx_type))
                print("module: tx.py, line: 44")
                raise SystemExit
            elif tx_type.lower() == "coinbase":
                coinbase_tx_in = Tx._parse_coinbase_tx_in(block_bytes_stream)
                tx_in_list.append(coinbase_tx_in)
            else:
                native_tx_in = Tx._parse_native_tx_in(block_bytes_stream)
                tx_in_list.append(native_tx_in)
        num_of_txs_out_int, num_of_txs_out_bytes = general_utils.read_varint(block_bytes_stream)
        tx_out_list = []
        for i in range(num_of_txs_out_int):  # loops through all txs out
            coinbase_tx_out = Tx._parse_tx_out(block_bytes_stream)
            tx_out_list.append(coinbase_tx_out)
        locktime = block_bytes_stream.read(tx_parameters["locktime"])
        subnetwork_id = block_bytes_stream.read(tx_parameters["subnetworkID"])
        if subnetwork_id == native_subnetwork_id:
            return Tx(version, num_of_txs_in_bytes, tx_in_list, num_of_txs_out_bytes, tx_out_list, locktime,
                      subnetwork_id)
        else:
            gas = block_bytes_stream.read(tx_parameters["gas"])
            payload_hash = block_bytes_stream.read(tx_parameters["payloadHash"])
            payload_length_int, payload_length_bytes = general_utils.read_varint(block_bytes_stream)
            payload = block_bytes_stream.read(payload_length_int)
            if tx_type.lower() == "coinbase":
                return Tx(version, num_of_txs_in_bytes, tx_in_list, num_of_txs_out_bytes, tx_out_list, locktime,
                          subnetwork_id, gas, payload_hash, payload_length_bytes, payload)
            else:
                return Tx(version, num_of_txs_in_bytes, tx_in_list, num_of_txs_out_bytes, tx_out_list, locktime,
                          subnetwork_id, gas, payload_hash, payload_length_bytes, payload)

    @staticmethod
    def _parse_coinbase_tx_in(block_bytes_stream):
        """
        Parse "coinbase tx in" data and returns as bytes array.

        :param block_bytes_stream: The bytes stream that holds the coinbase tx in data
        :return: Coinbase tx in as bytes array
        """
        tx_in_coinbase_parameters = {"prevTxID": 32, "prevTxIndex": 4, "coinbaseLen": "VARINT",
                                     "coinbase": "coinbaseLenInt", "sequence": 8}
        coinbase_tx_in_list = []
        previous_tx_id = block_bytes_stream.read(tx_in_coinbase_parameters["prevTxID"])
        previous_tx_index = block_bytes_stream.read(tx_in_coinbase_parameters["prevTxIndex"])
        coinbase_length_int, coinbase_length_bytes = general_utils.read_varint(block_bytes_stream)
        coinbase = block_bytes_stream.read(coinbase_length_int)
        sequence = block_bytes_stream.read(tx_in_coinbase_parameters["sequence"])
        coinbase_tx_in_list.extend([previous_tx_id, previous_tx_index, coinbase_length_bytes, coinbase, sequence])
        coinbase_tx_in = b"".join(coinbase_tx_in_list)
        return coinbase_tx_in

    @staticmethod
    def _parse_native_tx_in(block_bytes_stream):
        """
        Parse "native tx in" data and returns as bytes array.

        :param block_bytes_stream: The bytes stream that holds the native tx in data
        :return: Native tx in as bytes array
        """
        tx_in_parameters = {"prevTxID": 32, "prevTxIndex": 4, "scriptSigLen": "VARINT",
                            "SCRIPT_SIG": "scriptSigLen", "sequence": 8}
        tx_in_list = []
        previous_tx_id = block_bytes_stream.read(tx_in_parameters["prevTxID"])
        previous_tx_index = block_bytes_stream.read(tx_in_parameters["prevTxIndex"])
        script_sig_length_int, script_sig_length_bytes = general_utils.read_varint(block_bytes_stream)
        script_sig = block_bytes_stream.read(script_sig_length_int)
        sequence = block_bytes_stream.read(tx_in_parameters["sequence"])
        tx_in_list.extend([previous_tx_id, previous_tx_index, script_sig_length_bytes, script_sig, sequence])
        tx_in = b"".join(tx_in_list)
        return tx_in

    @staticmethod
    def _parse_tx_out(block_bytes_stream):
        """
        Parse "tx out" data and returns as bytes array.

        :param block_bytes_stream: The bytes stream that holds the tx out data
        :return: Tx out as bytes array
        """
        tx_out_parameters = {"value": 8, "scriptPubKeyLen": "VARINT", "SCRIPT_PUB_KEY": "scriptPubKeyLen"}
        tx_out_list = []
        value = block_bytes_stream.read(tx_out_parameters["value"])
        script_pub_key_len_int, script_pub_key_len_bytes = general_utils.read_varint(block_bytes_stream)
        script_pub_key = block_bytes_stream.read(script_pub_key_len_int)
        tx_out_list.extend([value, script_pub_key_len_bytes, script_pub_key])
        tx_out = b"".join(tx_out_list)
        return tx_out

    # ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!
    def update_version(self):
        pass

    def update_txs_in(self):
        pass

    def update_txs_out(self):
        pass

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
        self._tx_in = tx_in

    def set_number_of_txs_out(self, num_of_txs_out):
        """ Sets variable "_number_of_txs_out" to the received value"""
        self._number_of_txs_out = num_of_txs_out

    def set_txs_out(self, tx_out):
        """ Sets variable "_tx_out" to the received value"""
        self._tx_out = tx_out

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
        return self._tx_in

    def get_number_of_txs_out(self):
        """
        :return: Number of txs out as bytes
        """
        return self._number_of_txs_out

    def get_tx_out(self):
        """
        :return: Tx out as bytes
        """
        return self._tx_out

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
        tx_list.extend(
            [[self._version], [self._number_of_txs_in], self._tx_in, [self._number_of_txs_out], self._tx_out, [self._locktime],
             [self._subnetwork_id]])
        if self._subnetwork_id != native_subnetwork_id:
            tx_list.extend([[self._gas], [self._payload_hash], [self._payload_length], [self._payload]])
        tx_bytes = general_utils.flatten_nested_iterable(tx_list)
        return tx_bytes

    def get_tx_bytes_for_hash_merkle_root(self):
        """
        :return: Tx bytes array in a format specifically required for calculating the hash merkle root
        """
        tx_list = []
        tx_list.extend(
            [[self._version], [self._number_of_txs_in], self._tx_in, [self._number_of_txs_out], self._tx_out,
             [self._locktime],
             [self._subnetwork_id]])
        if self._subnetwork_id != native_subnetwork_id:
            tx_list.extend([[self._gas], [self._payload_hash], [b"\x00"]])
        tx_bytes = general_utils.build_element_from_list(tx_list)
        return tx_bytes
