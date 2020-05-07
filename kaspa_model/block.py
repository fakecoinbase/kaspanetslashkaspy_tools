from io import BytesIO
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspa_model.tx import Tx
from kaspy_tools.utils import general_utils

KT_logger = config_logger.get_kaspy_tools_logger()


class Block:
    """
    A kaspanet block.
    """

    def __init__(self, *, version_bytes=None, num_of_parent_blocks_bytes=None, parent_hashes=None,
                 hash_merkle_root_bytes=None, id_merkle_root_bytes=None, utxo_commitment_bytes=None,
                 timestamp_bytes=None, bits_bytes=None, nonce_bytes=None, num_of_txs_in_block_bytes=None,
                 coinbase_tx_bytes=None, native_tx_list_of_objs=None):
        """
        A constructor for a block. Due to historical reasons accept most fields in raw bytes form.
        Don't use it to create a new Block object.
        Instead, use the block_factory class method.
        :param version_bytes:  The Block version
        :param num_of_parent_blocks_bytes: Number of parent blocks
        :param parent_hashes: A list of hash values (already in bytes)
        :param hash_merkle_root_bytes: Hash Merkle root for the txs in this block.
        :param id_merkle_root_bytes:   Hash Merkle root for txs accepted by this block.
        :param utxo_commitment_bytes: UTXO commitment
        :param timestamp_bytes:  Timestamp (unix epoch) in bytes
        :param bits_bytes:    The 'bits' value used for mining.
        :param nonce_bytes:   The nonce value.
        :param num_of_txs_in_block_bytes:  A VarInt value (bytes) specifying the number of txs
                    present in this block (including coinbase).
        :param coinbase_tx_bytes:  The coinbase tx (in bytes)
        :param native_tx_list_of_objs: A list containing bytes representations of all native txs.
        """
        self._version_bytes = version_bytes
        self._version_int = None
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
        # self._nonce_int = int.from_bytes(self._nonce_bytes, byteorder='little')
        self._num_of_txs_in_block_int = None
        self._num_of_txs_in_block_bytes = num_of_txs_in_block_bytes
        self._coinbase_tx_obj = None
        self._coinbase_tx_bytes = coinbase_tx_bytes
        self._native_tx_list_of_objs = native_tx_list_of_objs

    @classmethod
    def block_factory(cls, *, version_int=None, version_bytes=None, num_of_parent_blocks=None, parent_hashes=None,
                      hash_merkle_root_bytes=None, id_merkle_root_bytes=None, utxo_commitment_bytes=None,
                      timestamp_int=None, timestamp_bytes=None, bits_bytes=None, bits_int=None,
                      nonce_bytes=None, num_of_txs_in_block_int=None, num_of_txs_in_block_bytes=None,
                      coinbase_tx_obj=None, coinbase_tx_bytes=None, native_tx_list_of_objs=None):
        """
        Use this method to create a new block.
        In general, if a field has a 'logical' and bytes values, you can specify just one of these.
        :param version:
        :param num_of_parent_blocks:
        :param parent_hashes:
        :param hash_merkle_root_bytes:
        :param id_merkle_root_bytes:
        :param utxo_commitment_bytes:
        :param timestamp_int:
        :param timestamp_bytes:
        :param bits_bytes:
        :param bits_int:
        :param nonce_bytes:
        :param num_of_txs_in_block_int:
        :param num_of_txs_in_block_bytes:
        :param coinbase_tx_obj:
        :param coinbase_tx_bytes:
        :param native_tx_list_of_objs:
        :return:  A new Block
        """
        new_block = cls()
        new_block._version_int = version_int
        new_block._version_bytes = version_bytes
        new_block._number_of_parent_blocks = num_of_parent_blocks
        new_block._parent_hashes = parent_hashes
        new_block._hash_merkle_root_bytes = hash_merkle_root_bytes
        new_block._id_merkle_root_bytes = id_merkle_root_bytes
        new_block._utxo_commitment_bytes = utxo_commitment_bytes
        new_block._timestamp_int = timestamp_int
        new_block._timestamp_bytes = timestamp_bytes
        new_block._bits_int = bits_int
        new_block._bits_bytes = bits_bytes
        if nonce_bytes == None:
            new_block._nonce_bytes = b'\x00' * 8
            new_block._nonce_int = 0
        else:
            new_block._nonce_bytes = nonce_bytes
            new_block._nonce_int = int.from_bytes(new_block.nonce_bytes, byteorder='little')

        new_block._coinbase_tx_obj = coinbase_tx_obj
        new_block._coinbase_tx_bytes = coinbase_tx_bytes
        if native_tx_list_of_objs==None:
            new_block._native_tx_list_of_objs = []
        else:
            new_block._native_tx_list_of_objs = native_tx_list_of_objs

        new_block.num_of_txs_in_block_int = len(new_block.native_tx_list_of_objs) + 1
        return new_block

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
                     num_of_txs_in_block_bytes=block_body[0], coinbase_tx_bytes=block_body[1],
                     native_tx_list_of_objs=block_body[2])

    @staticmethod
    def _parse_block_header(block_bytes_stream):
        """
        Parse the block's header from the provided bytes stream and returns it as a bytes list

        :param block_bytes_stream: The bytes stream that holds the block data
        :return: Block header as a list
        """
        header_parameters = {"version": 4, "numParentBlocks": 1, "parentHashes": 32, "hashMerkleRoot": 32,
                             "idMerkleRoot": 32, "utxoCommitment": 32, "timeStamp": 8, "bits": 4, "nonce": 8}

        version_bytes = block_bytes_stream.read(header_parameters["version"])
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
        return [version_bytes, num_of_parent_blocks, parent_hashes, hash_merkle_root_bytes, id_merkle_root_bytes,
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

        native_tx_list_of_objs = []
        for i in range(num_of_txs_in_block_int - 1):
            native_tx_obj = Tx.parse_tx(block_bytes_stream)
            native_tx_list_of_objs.append(native_tx_obj)

        return [num_of_txs_in_block_bytes, coinbase_tx_obj, native_tx_list_of_objs]

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

    # ========== Get Block Methods ========== #

    @property
    def version_int(self):
        """
        Get the value of the version field as an int.
        :return: version as int
        """
        if (self._version_int == None) and (self._version_bytes != None):
            self._version_int = int.from_bytes(self._version_bytes, byteorder='little')
        return self._version_int

    @property
    def version_bytes(self):
        """
        Get the value of version as bytes.
        :return: version as bytes
        """
        if (self._version_bytes == None) and (self._version_int != None):
            self.version_bytes = self._version_int.to_bytes(4, byteorder='little')
        return self._version_bytes

    @property
    def number_of_parent_blocks_bytes(self):
        """
        Gets the number of parents.
        :return: Number of parents as a single byte
        """
        if not self._number_of_parent_blocks_bytes:
            self._number_of_parent_blocks_bytes = self._number_of_parent_blocks.to_bytes(1, byteorder='little')

        return self._number_of_parent_blocks_bytes

    @property
    def parent_hashes(self):
        """
        Gets parent hash value.
        :return: A list with the hashes (as bytes)
        """
        return self._parent_hashes

    @property
    def hash_merkle_root_bytes(self):
        """
        Gets the Merkle root value of txs in this block.
        :return: Bytes representation of Merkle root
        """
        return self._hash_merkle_root_bytes

    @property
    def id_merkle_root_bytes(self):
        """
        Gets the Merkle root value of txs accepted in this block.
        :return: A bytes representation of Merkle root.
        """
        return self._id_merkle_root_bytes

    @property
    def utxo_commitment_bytes(self):
        """
        Get UTXO commitment
        :return: A bytes value of the UTXO commitment.
        """
        return self._utxo_commitment_bytes

    @property
    def timestamp_int(self):
        """
        Gets UNIX epoch timestamp.
        :return: Epoch as int.
        """
        if (not self._timestamp_int) and (self._timestamp_bytes != None):
            self._timestamp_int = int.from_bytes(self._timestamp_bytes, byteorder='little')
        return self._timestamp_int

    @property
    def timestamp_bytes(self):
        """
        Gets UNIX epoch timestamp.
        :return: Epoch as bytes.
        """
        if (not self._timestamp_bytes) and (self._timestamp_int != None):
            self._timestamp_bytes = (self._timestamp_int).to_bytes(8, byteorder='little')
        return self._timestamp_bytes

    @property
    def bits_bytes(self):
        """
        Gets the 'bits' value.
        :return: The 'bits' value (bytes).
        """
        if (not self._bits_bytes) and (self._bits_int != None):
            self._bits_bytes = (self._bits_int).to_bytes(4, byteorder='little')
        return self._bits_bytes

    @property
    def bits_int(self):
        """
        Gets the 'bits' balue.
        :return: The 'bits' value (int).
        """
        if (not self._bits_int) and (self._bits_bytes != None):
            self._bits_int = int.from_bytes(self._bits_bytes, byteorder='little')
        return self._bits_int

    @property
    def nonce_bytes(self):
        """
        Get the 'nonce' value
        :return: 'nonce as bytes
        """
        return self._nonce_bytes

    @property
    def nonce_int(self):
        """
        Get the 'nonce' value
        :return: 'nonce as int
        """
        return self._nonce_int

    @property
    def target_int(self):
        nonce_int = self.nonce_int
        exponent = self.bits_bytes[-1]
        coefficient = int.from_bytes(self.bits_bytes[:-1], "little")
        target = coefficient * 256 ** (exponent - 3)
        return target

    @property
    def block_header_hash(self):
        dbl_hash = general_utils.hash_256(self.block_header_bytes)
        block_hash = int.from_bytes(dbl_hash, "little")
        return block_hash

    @property
    def num_of_txs_in_block_int(self):
        """
        Gets the number of Txs in this block
        :return: A VarInt value
        """
        if (self._num_of_txs_in_block_int == None) and (self._num_of_txs_in_block_bytes != None):
            self._num_of_txs_in_block_int = general_utils.read_varint(BytesIO(self._num_of_txs_in_block_bytes))
        return self._num_of_txs_in_block_int

    @property
    def num_of_txs_in_block_bytes(self):
        """
        Gets the number of Txs in this block
        :return: bytes representation of this number.
        """
        if (self._num_of_txs_in_block_bytes == None) and (self._num_of_txs_in_block_int != None):
            self._num_of_txs_in_block_bytes = general_utils.write_varint(self._num_of_txs_in_block_int)
        return self._num_of_txs_in_block_bytes

    @property
    def coinbase_tx_obj(self):
        """
        The single coinbase Tx in this block
        :return: coinbase Tx as a Tx object
        """
        if (self._coinbase_tx_obj == None) and (self._coinbase_tx_bytes != None):
            self._coinbase_tx_obj = Tx.parse_tx(self._coinbase_tx_bytes)
        return self._coinbase_tx_obj

    @property
    def coinbase_tx_bytes(self):
        """
        The single coinbase Tx in this block
        :return: coinbase Tx as a bytes object.
        """
        if (self._coinbase_tx_bytes == None) and (self._coinbase_tx_obj != None):
            self._coinbase_tx_bytes = bytes(self._coinbase_tx_obj)
        return self._coinbase_tx_bytes

    @property
    def native_tx_list_of_objs(self):
        """
        Gets a list of native tx in this block.
        :return: a list of Tx objs
        """
        return self._native_tx_list_of_objs

    # ========== Set Methods ========== #

    @version_bytes.setter
    def version_bytes(self, version_bytes):
        """
        Set 'version'
        :param version_bytes: version in bytes
        :return: None
        """
        self._version_bytes = version_bytes

    @version_int.setter
    def version_int(self, version_int):
        """
        Set 'version'
        :param version_bytes: version as an int
        :return: None
        """
        self._version_int = version_int

    @number_of_parent_blocks_bytes.setter
    def number_of_parent_blocks_bytes(self, number_of_parent_blocks_bytes):
        """
        Sets number of parents
        :param number_of_parent_blocks_bytes:
        :return: None
        """
        self._number_of_parent_blocks_bytes = number_of_parent_blocks_bytes

    @parent_hashes.setter
    def parent_hashes(self, parent_hashes):
        """
        Sets the list of parent hashes.
        :param parent_hashes: List of hashes (bytes)
        :return: None
        """
        self._parent_hashes = parent_hashes

    @hash_merkle_root_bytes.setter
    def hash_merkle_root_bytes(self, hash_merkle_root_bytes):
        """
        Sets the Merkle root
        :param hash_merkle_root_bytes:
        :return: None
        """
        self._hash_merkle_root_bytes = hash_merkle_root_bytes

    @id_merkle_root_bytes.setter
    def id_merkle_root_bytes(self, id_merkle_root_bytes):
        """
        Sets the accepted id Merkle root
        :param id_merkle_root_bytes:
        :return: None
        """
        self._id_merkle_root_bytes = id_merkle_root_bytes

    @utxo_commitment_bytes.setter
    def utxo_commitment_bytes(self, utxo_commitment_bytes):
        """
        Sets the UTXO commitment
        :param utxo_commitment_bytes:
        :return: None
        """
        self._utxo_commitment_bytes = utxo_commitment_bytes

    @timestamp_bytes.setter
    def timestamp_bytes(self, timestamp_bytes):
        """
        Sets the timestamp (bytes)
        :param timestamp_bytes:
        :return: None
        """
        self._timestamp_bytes = timestamp_bytes

    @timestamp_int.setter
    def timestamp_int(self, timestamp_int):
        """
        Sets the timestamp (int)
        :param timestamp_int:
        :return: None
        """
        self._timestamp_int = timestamp_int

    @bits_int.setter
    def bits_int(self, bits_int):
        """
        Sets the 'bits' value (int).
        :param bits_int:
        :return: None
        """
        self._bits_int = bits_int

    @bits_bytes.setter
    def bits_bytes(self, bits_bytes):
        """
        Sets the 'bits' value (bytes)
        :param bits_bytes:
        :return: None
        """
        self._bits_bytes = bits_bytes

    @nonce_bytes.setter
    def nonce_bytes(self, nonce_bytes):
        """
        Sets 'nonce'
        :param nonce_bytes:
        :return: None
        """
        self._nonce_bytes = nonce_bytes

    @nonce_int.setter
    def nonce_int(self, nonce_int):
        """
        Sets 'nonce'
        :param nonce_bytes:
        :return: None
        """
        self._nonce_int = nonce_int
        self.nonce_bytes = self._nonce_int.to_bytes(8, byteorder='little')

    @num_of_txs_in_block_int.setter
    def num_of_txs_in_block_int(self, num_of_txs_in_block_int):
        """
        Sets number of txs in block (int)
        :param num_of_txs_in_block_int:
        :return: None
        """
        self._num_of_txs_in_block_int = num_of_txs_in_block_int

    @num_of_txs_in_block_bytes.setter
    def num_of_txs_in_block_bytes(self, num_of_txs_in_block_bytes):
        """
        Sets number of txs in block (bytes)
        :param num_of_txs_in_block_int:
        :return: None
        """
        self._num_of_txs_in_block_bytes = num_of_txs_in_block_bytes

    @coinbase_tx_obj.setter
    def coinbase_tx_obj(self, coinbase_tx_obj):
        """
        Sets coinbase tx into block (tx as obj)
        :param coinbase_tx_obj:
        :return: None
        """
        self._coinbase_tx_obj = coinbase_tx_obj

    @coinbase_tx_bytes.setter
    def coinbase_tx_bytes(self, coinbase_tx_bytes):
        """
        Sets coinbase tx into block (tx as bytes)
        :param coinbase_tx_obj:
        :return: None
        """
        self._coinbase_tx_bytes = coinbase_tx_bytes

    @native_tx_list_of_objs.setter
    def native_tx_list_of_objs(self, native_tx_list_of_objs):
        """
        Sets list of native tx (objects)
        :param native_tx_list_of_objs:
        :return:
        """
        self._native_tx_list_of_objs = native_tx_list_of_objs

    def add_native_transaction(self, tx_obj):
        self.num_of_txs_in_block_int += 1
        temp = self.num_of_txs_in_block_bytes   # to update it
        self.native_tx_list_of_objs.append(tx_obj)


    # def get_block_header_list(self):
    #     """
    #     :return: Block header bytes as a list
    #     """
    #     return [self._version_bytes, self._number_of_parent_blocks_bytes, self._parent_hashes,
    #             self._hash_merkle_root_bytes, self._id_merkle_root_bytes, self._utxo_commitment_bytes,
    #             self._timestamp_bytes, self._bits_bytes, self._nonce_bytes]

    @property
    def block_header_bytes(self):
        """
        :return: Block header bytes object
        """
        block_header_bytes = self._version_bytes + self._number_of_parent_blocks_bytes + \
                             b''.join(self.parent_hashes) + self.hash_merkle_root_bytes + \
                             self.id_merkle_root_bytes + self.utxo_commitment_bytes + \
                             self.timestamp_bytes + self.bits_bytes + self.nonce_bytes
        return block_header_bytes

    def get_block_body_list(self):
        """
        :return: Block body bytes as a list
        """
        coinbase_tx_list = self._coinbase_tx_obj.get_tx_bytes()
        native_txs_list = []
        for tx in self._native_tx_list_of_objs:
            native_tx_bytes = tx.get_tx_bytes()
            native_txs_list.append(native_tx_bytes)
        return [self.num_of_txs_in_block_bytes, coinbase_tx_list, native_txs_list]

    def get_block_body_bytes_array(self):
        """
        :return: Block body bytes as an array
        """
        block_body_list = self.get_block_body_list()
        block_body_bytes_array = general_utils.build_element_from_list(block_body_list)
        return block_body_bytes_array

    @property
    def block_txs_list_as_bytes(self):
        """
        Returns the Txs bytes as a list, not including the "payload length" & the "payload".

        :return: Txs bytes as a list
        """
        txs_list = []
        # first append the coinbase tx
        txs_list.append(self._coinbase_tx_obj.get_tx_bytes_for_hash_merkle_root())
        for tx in self._native_tx_list_of_objs:
            # native_tx_bytes = tx.get_tx_bytes_for_hash_merkle_root()
            native_tx_bytes = tx.get_tx_bytes_for_hash_merkle_root()
            txs_list.append(native_tx_bytes)
        return txs_list
