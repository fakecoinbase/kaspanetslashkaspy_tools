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
                 coinbase_tx_bytes=None, native_tx_list=None):
        self._version_bytes = version_bytes
        self._version = None
        self._number_of_parent_blocks = None
        self._number_of_parent_blocks_bytes = num_of_parent_blocks_bytes
        self._parent_hashes = parent_hashes
        self._hash_merkle_root_bytes = hash_merkle_root_bytes
        self._id_merkle_root_bytes = id_merkle_root_bytes
        self._utxo_commitment_bytes = utxo_commitment_bytes
        self._timestamp_bytes = timestamp_bytes
        self._bits_int = None
        self._bits_bytes = bits_bytes
        self._nonce_bytes = nonce_bytes
        self._num_of_txs_in_block_int = None
        self._num_of_txs_in_block_bytes = num_of_txs_in_block_bytes
        self._coinbase_tx_obj=None
        self._coinbase_tx_bytes = coinbase_tx_bytes
        self._native_txs = native_tx_list

    @classmethod
    def block_factory(cls, *, version=None, num_of_parent_blocks=None, parent_hashes=None,
                      hash_merkle_root_bytes=None, id_merkle_root_bytes=None, utxo_commitment_bytes=None,
                      timestamp_int=None, timestamp_bytes=None, bits_bytes=None, bits_int=None,
                      nonce_bytes=None, num_of_txs_in_block_int=None, num_of_txs_in_block_bytes=None,
                      coinbase_tx_obj=None, coinbase_tx_bytes=None):
        new_block = cls()
        new_block._version = version
        new_block._number_of_parent_blocks = num_of_parent_blocks
        new_block._parent_hashes = parent_hashes
        new_block._hash_merkle_root_bytes = hash_merkle_root_bytes
        new_block._id_merkle_root_bytes = id_merkle_root_bytes
        new_block._utxo_commitment_bytes = utxo_commitment_bytes
        new_block._timestamp_int = timestamp_int
        new_block._timestamp_bytes = timestamp_bytes
        new_block._bits_int = bits_int
        new_block._bits_bytes = bits_bytes
        new_block._nonce_bytes = nonce_bytes
        new_block._num_of_txs_in_block_int = num_of_txs_in_block_int
        new_block._num_of_txs_in_block_bytes = num_of_txs_in_block_bytes
        new_block._coinbase_tx_obj = coinbase_tx_obj
        new_block._coinbase_tx_bytes = coinbase_tx_bytes
        new_block._native_txs = native_tx_list

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
                     parent_hashes=block_header[2], hash_merkle_root_bytes=block_header[3],
                     id_merkle_root_bytes=block_header[4], utxo_commitment_bytes=block_header[5],
                     timestamp_bytes=block_header[6], bits_bytes=block_header[7], nonce_bytes=block_header[8],
                     num_of_txs_in_block_bytes=block_body[0], coinbase_tx_bytes=block_body[1], native_tx_list=block_body[2])

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

        hash_merkle_root_bytes = block_bytes_stream.read(header_parameters["hashMerkleRoot"])
        id_merkle_root_bytes = block_bytes_stream.read(header_parameters["idMerkleRoot"])
        utxo_commitment_bytes = block_bytes_stream.read(header_parameters["utxoCommitment"])
        timestamp_bytes = block_bytes_stream.read(header_parameters["timeStamp"])
        bits_bytes = block_bytes_stream.read(header_parameters["bits"])
        nonce_bytes = block_bytes_stream.read(header_parameters["nonce"])
        return [version, num_of_parent_blocks, parent_hashes, hash_merkle_root_bytes, id_merkle_root_bytes,
                utxo_commitment_bytes, timestamp_bytes, bits_bytes, nonce_bytes]

    @staticmethod
    def _parse_block_body(block_bytes_stream):
        """
        Parse the block's body bytes from the provided stream and returns it as a bytes list

        :param block_bytes_stream: The bytes stream that holds the block body data
        :return: Block body as a list
        """
        num_of_txs_in_block_int, num_of_txs_in_block_bytes = general_utils.read_varint(block_bytes_stream)

        coinbase_tx_obj = Tx.parse_tx(block_bytes_stream)

        native_txs_list = []
        for i in range(num_of_txs_in_block_int - 1):
            native_tx = Tx.parse_tx(block_bytes_stream)
            native_txs_list.append(native_tx)

        return [num_of_txs_in_block_bytes, coinbase_tx_obj, native_txs_list]

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

    @property
    def version_bytes(self):
        """ Gets variable "_version_bytes" to the received value"""
        if self._version_bytes:
            return self._version_bytes
        else:
            return self._version.to_bytes(4, byteorder='little')

    @property
    def number_of_parent_blocks_bytes(self):
        """ Gets variable "number of parent blocks" to the received value"""
        if not self._number_of_parent_blocks_bytes:
            self._number_of_parent_blocks_bytes = self._number_of_parent_blocks.to_bytes(1, byteorder='little')

        return self._number_of_parent_blocks_bytes

    @property
    def parent_hashes(self):
        """ Sets variable "parent hashes" to the received value"""
        return self._parent_hashes

    @property
    def hash_merkle_root_bytes(self):
        return self._hash_merkle_root_bytes

    @property
    def id_merkle_root_bytes(self):
        """ Gets variable "id merkle root" to the received value"""
        return self._id_merkle_root_bytes

    @property
    def utxo_commitment_bytes(self):
        return self._utxo_commitment_bytes

    @property
    def timestamp_int(self):
        if (not self._timestamp_int) and (self._timestamp_bytes!=None):
            self._timestamp_int = int.from_bytes(self._timestamp_bytes, byteorder='little')
        return self._timestamp_int

    @property
    def timestamp_bytes(self):
        if (not self._timestamp_bytes) and (self._timestamp_int!=None):
            self._timestamp_bytes = (self._timestamp_int).to_bytes(8, byteorder='little')
        return self._timestamp_bytes

    @property
    def bits_bytes(self):
        if (not self._bits_bytes) and (self._bits_int != None):
            self._bits_bytes = (self._bits_int).to_bytes(4, byteorder='little')
        return self._bits_bytes

    @property
    def bits_int(self):
        if (not self._bits_int) and (self._bits_bytes != None):
            self._bits_int = int.from_bytes(self._bits_bytes, byteorder='little')
        return self._bits_int

    @property
    def nonce_bytes(self):
        return self._nonce_bytes

    @property
    def num_of_txs_in_block_int(self):
        if (self._num_of_txs_in_block_int == None) and (self._num_of_txs_in_block_bytes != None):
            self._num_of_txs_in_block_int = general_utils.read_varint(BytesIO(self._num_of_txs_in_block_bytes))
        return self._num_of_txs_in_block_int

    @property
    def num_of_txs_in_block_bytes(self):
        if (self._num_of_txs_in_block_bytes == None) and (self._num_of_txs_in_block_int != None):
            self._num_of_txs_in_block_bytes = general_utils.write_varint(self._num_of_txs_in_block_int)
        return self._num_of_txs_in_block_bytes

    @property
    def coinbase_tx_obj(self):
        if (self._coinbase_tx_obj == None) and (self._coinbase_tx_bytes != None):
            self._coinbase_tx_obj = Tx.parse_tx(self._coinbase_tx_bytes)
        return self._coinbase_tx_obj

    @property
    def coinbase_tx_bytes(self):
        if (self._coinbase_tx_bytes == None) and (self._coinbase_tx_obj != None):
            self._coinbase_tx_bytes = bytes(self._coinbase_tx_obj)
        return self._coinbase_tx_bytes

    def set_native_txs(self):
        pass

    # ========== Get Methods ========== #

    @version_bytes.setter
    def version_bytes(self, version_bytes):
        """
        :return: Version as bytes
        """
        self._version_bytes = version_bytes

    @number_of_parent_blocks_bytes.setter
    def number_of_parent_blocks_bytes(self, number_of_parent_blocks_bytes):
        """
        :return: None
        """
        self._number_of_parent_blocks_bytes = number_of_parent_blocks_bytes

    @parent_hashes.setter
    def parent_hashes(self, parent_hashes):
        self._parent_hashes = parent_hashes

    @hash_merkle_root_bytes.setter
    def hash_merkle_root_bytes(self, hash_merkle_root_bytes):
        self._hash_merkle_root_bytes = hash_merkle_root_bytes

    @id_merkle_root_bytes.setter
    def id_merkle_root_bytes(self, id_merkle_root_bytes):
        self._id_merkle_root_bytes = id_merkle_root_bytes

    @utxo_commitment_bytes.setter
    def utxo_commitment_bytes(self, utxo_commitment_bytes):
        self._utxo_commitment_bytes = utxo_commitment_bytes

    @timestamp_bytes.setter
    def timestamp_bytes(self, timestamp_bytes):
        self._timestamp_bytes = timestamp_bytes

    @timestamp_int.setter
    def timestamp_int(self, timestamp_int):
        self._timestamp_int = timestamp_int

    @bits_int.setter
    def bits_int(self, bits_int):
        self._bits_int = bits_int

    @bits_bytes.setter
    def bits_bytes(self, bits_bytes):
        self._bits_bytes = bits_bytes

    @nonce_bytes.setter
    def nonce_bytes(self, nonce_bytes):
        self._nonce_bytes = nonce_bytes

    @num_of_txs_in_block_int.setter
    def num_of_txs_in_block_int(self, num_of_txs_in_block_int):
        self._num_of_txs_in_block_int = num_of_txs_in_block_int

    @num_of_txs_in_block_bytes.setter
    def num_of_txs_in_block_bytes(self, num_of_txs_in_block_bytes):
        self._num_of_txs_in_block_bytes = num_of_txs_in_block_bytes

    @coinbase_tx_obj.setter
    def coinbase_tx_obj(self, coinbase_tx_obj):
        self._coinbase_tx_obj = coinbase_tx_obj

    @coinbase_tx_bytes.setter
    def coinbase_tx_bytes(self, coinbase_tx_bytes):
        self._coinbase_tx_bytes = coinbase_tx_bytes

    def get_native_txs(self):
        """
        :return: List of all the native txs class objects
        """
        return self._native_txs

    def get_block_header_list(self):
        """
        :return: Block header bytes as a list
        """
        return [self._version_bytes, self._number_of_parent_blocks_bytes, self._parent_hashes,
                self._hash_merkle_root_bytes, self._id_merkle_root_bytes, self._utxo_commitment_bytes,
                self._timestamp_bytes, self._bits_bytes, self._nonce_bytes]

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
        coinbase_tx_list = self._coinbase_tx_obj.get_tx_bytes()
        native_txs_list = []
        for tx in self._native_txs:
            native_tx_list = tx.get_tx_bytes()
            native_txs_list.append(native_tx_list)
        return [self._num_of_txs_in_block_bytes, coinbase_tx_list, native_txs_list]

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
        coinbase_tx_bytes = self._coinbase_tx_obj.get_tx_bytes_for_hash_merkle_root()
        txs_list = []
        for tx in self._native_txs:
            native_tx_bytes = tx.get_tx_bytes_for_hash_merkle_root()
            txs_list.append(native_tx_bytes)
        txs_list.insert(0, coinbase_tx_bytes)
        return txs_list
