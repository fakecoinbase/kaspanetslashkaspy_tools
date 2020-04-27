
from io import BytesIO
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspa_model.tx import Tx
from kaspy_tools.utils import general_utils

KT_logger = config_logger.get_kaspy_tools_logger()

class Block:
    """
    This objects holds all the required methods to handle block data.
    """
    def __init__(self, *, version_bytes=None, num_of_parent_blocks_bytes=None, parent_hashes=None,
                 hash_merkle_root_bytes=None, id_merkle_root_bytes=None, utxo_commitment_bytes=None,
                 timestamp_bytes=None, bits_bytes=None, nonce_bytes=None, num_of_txs_in_block_bytes=None,
                 coinbase_tx=None, native_tx_list=None):
        self._version = version_bytes
        self._number_of_parent_blocks = num_of_parent_blocks_bytes
        self._parent_hashes = parent_hashes
        self._hash_merkle_root = hash_merkle_root_bytes
        self._id_merkle_root = id_merkle_root_bytes
        self._utxo_commitment = utxo_commitment_bytes
        self._timestamp = timestamp_bytes
        self._bits = bits_bytes
        self._nonce = nonce_bytes
        self._num_of_txs_in_block = num_of_txs_in_block_bytes
        self._coinbase_tx = coinbase_tx
        self._native_txs = native_tx_list

    # ========== Parsing Methods ========== #

    @staticmethod
    def parse_block(block_bytes):
        """
        Parse the block data into "block header" and "block body".
        Returns a Block class object with the parsed information.

        :param block_bytes: The block data as bytes
        :return: Block class object
        """
        block_stream = BytesIO(block_bytes)
        block_header = Block._parse_block_header(block_stream)
        block_body = Block._parse_block_body(block_stream)
        return Block(version_bytes=block_header[0], num_of_parent_blocks_bytes=block_header[1],
                     parent_hashes= block_header[2], hash_merkle_root_bytes= block_header[3],
                     id_merkle_root_bytes=block_header[4], utxo_commitment_bytes=block_header[5],
                     timestamp_bytes=block_header[6], bits_bytes=block_header[7], nonce_bytes=block_header[8],
                     num_of_txs_in_block_bytes=block_body[0], coinbase_tx=block_body[1], native_tx_list=block_body[2])

    @staticmethod
    def _parse_block_header(block_bytes_stream):
        """
        Parse the block's header from the provided bytes stream and returns it as a bytes list

        :param block_bytes_stream: The bytes stream that holds the block data
        :return: Block header as a list
        """
        header_parameters = {"version": 4, "numParentBlocks": 1, "parentHashes": 32, "hashMerkleRoot": 32,
                             "idMerkleRoot": 32, "utxoCommitment": 32, "timeStamp": 8, "bits": 4, "nonce": 8}

        version = block_bytes_stream.read(header_parameters["version"])
        num_of_parent_blocks = block_bytes_stream.read(header_parameters["numParentBlocks"])
        num_of_parent_blocks_int = general_utils.int_from_little_endian(num_of_parent_blocks)
        parent_hashes_to_get = num_of_parent_blocks_int
        parent_hashes = []
        while parent_hashes_to_get != 0:
            p_hash = block_bytes_stream.read(header_parameters["parentHashes"])
            parent_hashes.append(p_hash)
            parent_hashes_to_get -= 1

        hash_merkle_root = block_bytes_stream.read(header_parameters["hashMerkleRoot"])
        id_merkle_root = block_bytes_stream.read(header_parameters["idMerkleRoot"])
        utxo_commitment = block_bytes_stream.read(header_parameters["utxoCommitment"])
        timestamp = block_bytes_stream.read(header_parameters["timeStamp"])
        bits = block_bytes_stream.read(header_parameters["bits"])
        nonce = block_bytes_stream.read(header_parameters["nonce"])
        return [version, num_of_parent_blocks, parent_hashes, hash_merkle_root, id_merkle_root, utxo_commitment,
                timestamp, bits, nonce]

    @staticmethod
    def _parse_block_body(block_bytes_stream):
        """
        Parse the block's body bytes from the provided stream and returns it as a bytes list

        :param block_bytes_stream: The bytes stream that holds the block body data
        :return: Block body as a list
        """
        num_of_txs_in_block_int, num_of_txs_in_block_bytes = general_utils.read_varint(block_bytes_stream)

        coinbase_tx = Tx.parse_tx(block_bytes_stream)

        native_txs_list = []
        for i in range(num_of_txs_in_block_int - 1):
            native_tx = Tx.parse_tx(block_bytes_stream)
            native_txs_list.append(native_tx)

        return [num_of_txs_in_block_bytes, coinbase_tx, native_txs_list]

    # ========== Rebuilding Methods ========== #

    @staticmethod
    def rebuild_block(block_header, block_body):
        """
        Returns the full block as bytes.

        :param block_header: Block header as bytes
        :param block_body: Block body as bytes
        :return: Full block as bytes
        """
        return block_header + block_body

    # ========== Set Block Methods ========== #

    def set_version(self, version):
        """ Sets variable "_version" to the received value"""
        self._version = version

    def set_number_of_parent_blocks(self, num_of_parent_blocks):
        """ Sets variable "number of parent blocks" to the received value"""
        self._number_of_parent_blocks = num_of_parent_blocks

    def set_parent_hashes(self, parent_hashes):
        """ Sets variable "parent hashes" to the received value"""
        self._parent_hashes = parent_hashes

    def set_hash_merkle_root(self, hash_merkle_root):
        """ Sets variable "hash merkle root" to the received value"""
        self._hash_merkle_root = hash_merkle_root

    def set_id_merkle_root(self, id_merkle_root):
        """ Sets variable "id merkle root" to the received value"""
        self._id_merkle_root = id_merkle_root

    def set_utxo_commitment(self, utxo_commitment):
        """ Sets variable "utxo commitment" to the received value"""
        self._utxo_commitment = utxo_commitment

    def set_timestamp(self, timestamp):
        """ Sets variable "_timestamp" to the received value"""
        self._timestamp = timestamp

    def set_bits(self, bits):
        """ Sets variable "_bits" to the received value"""
        self._bits = bits

    def set_nonce(self, nonce):
        """ Sets variable "_nonce" to the received value"""
        self._nonce = nonce

    def set_num_of_txs_in_block(self, num_of_txs_in_block):
        """ Sets variable "num of txs in block" to the received value"""
        self._num_of_txs_in_block = num_of_txs_in_block

    def set_coinbase_tx(self, coinbase_tx_object):
        self._coinbase_tx = coinbase_tx_object

    def set_native_txs(self):
        pass

    # ========== Get Methods ========== #

    def get_version(self):
        """
        :return: Version as bytes
        """
        return self._version

    def get_number_of_parent_blocks(self):
        """
        :return: Number of parent blocks as bytes
        """
        return self._number_of_parent_blocks

    def get_parent_hashes(self):
        """
        :return: Parent hashes as bytes
        """
        return self._parent_hashes

    def get_hash_merkle_root(self):
        """
        :return: Hash merkle root as bytes
        """
        return self._hash_merkle_root

    def get_id_merkle_root(self):
        """
        :return: ID merkle root as bytes
        """
        return self._id_merkle_root

    def get_utxo_commitment(self):
        """
        :return: Utxo commitment as bytes
        """
        return self._utxo_commitment

    def get_timestamp(self):
        """
        :return: Timestamp as bytes
        """
        return self._timestamp

    def get_bits(self):
        """
        :return:  Bits as bytes
        """
        return self._bits

    def get_nonce(self):
        """
        :return: Nonce as bytes
        """
        return self._nonce

    def get_num_of_txs_in_block(self):
        """
        :return: Number of "txs in" in the block as bytes
        """
        return self._num_of_txs_in_block

    def get_coinbase_tx(self):
        """
        :return: Coinbase tx class object
        """
        return self._coinbase_tx

    def get_native_txs(self):
        """
        :return: List of all the native txs class objects
        """
        return self._native_txs

    def get_block_header_list(self):
        """
        :return: Block header bytes as a list
        """
        return [self._version, self._number_of_parent_blocks, self._parent_hashes, self._hash_merkle_root,
                self._id_merkle_root, self._utxo_commitment, self._timestamp, self._bits, self._nonce]

    def get_block_header_bytes_array(self):
        """
        :return: Block header bytes as an array
        """
        block_header_list = self.get_block_header_list()
        block_header_bytes_array = general_utils.build_element_from_list(block_header_list)
        return block_header_bytes_array

    def get_block_body_list(self):
        """
        :return: Block body bytes as a list
        """
        coinbase_tx_list = self._coinbase_tx.get_tx_bytes()
        native_txs_list = []
        for tx in self._native_txs:
            native_tx_list = tx.get_tx_bytes()
            native_txs_list.append(native_tx_list)
        return [self._num_of_txs_in_block, coinbase_tx_list, native_txs_list]

    def get_block_body_bytes_array(self):
        """
        :return: Block body bytes as an array
        """
        block_body_list = self.get_block_body_list()
        block_body_bytes_array = general_utils.build_element_from_list(block_body_list)
        return block_body_bytes_array

    def get_block_txs_list_for_hash_merkle_root(self):
        """
        Returns the Txs bytes as a list, not including the "payload length" & the "payload".

        :return: Txs bytes as a list
        """
        coinbase_tx_bytes = self._coinbase_tx.get_tx_bytes_for_hash_merkle_root()
        txs_list = []
        for tx in self._native_txs:
            native_tx_bytes = tx.get_tx_bytes_for_hash_merkle_root()
            txs_list.append(native_tx_bytes)
        txs_list.insert(0, coinbase_tx_bytes)
        return txs_list
