"""
This module holds all the UPDATE methods for the automation project.
"""

import random
from io import BytesIO
import time
from kaspy_tools.kaspa_crypto.merkle_root import MerkleTree
from kaspy_tools.kaspad import kaspad_constants
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.kaspa_model.tx import Tx
from kaspy_tools.utils import general_utils


# ========== Update Block Methods ========== #

def update_all_valid_block_variables(block_object, block_template, conn=None, native_txs=None, netprefix='kaspadev'):
    """
    Initiates the VALID updating process for the entire block

    :param block_object: The block object that holds the variables to update
    :param block_template: Template from getBlockTemplate request
    :param conn: connection details
    :param native_txs: A list of native transactions to include
    """
    update_block_version(block_object, block_template)
    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template, native_txs)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_using_invalid_version_data(block_object, version_int, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "version" value.

    :param version_int: The required version as an int
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']
    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_version(block_object, 5)  # temporary int

    update_nonce(block_object)
    if version_int is None:
        update_version_invalid(block_object)
    else:
        update_version(block_object, version_int)


def update_block_variables_without_parent_block_data(block_object, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, ignoring "parent block data" variables

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    block_object.number_of_parent_blocks = 1
    block_object.parent_hashes = [b'12345678901234567890123456789012']
    update_nonce(block_object)


def update_block_variables_without_txs(block_object, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, ignoring "Txs" objects

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_hash_merkle_root(block_object, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, ignoring "hash merkle root" variable

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_id_merkle_root(block_object, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, ignoring "ID merkle root" variable

    :param block_object: The block object that holds the variables to update
    :param conn: connection details
    :param pay_address: paying address for block
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_utxo_commitment(block_object, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, ignoring "utxo commitment" variable

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_with_an_invalid_timestamp(block_object, timestamp_value, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "timestamp" value.

    :param timestamp_value: The value to use as the invalid timestamp
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp_invalid(block_object, timestamp_value)
    update_bits(block_object, block_template)
    block_object.version_int = 0x10000000
    update_nonce(block_object)


def update_block_variables_with_an_invalid_bits(block_object, bits_value, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "bits" value.

    :param bits_value: The value to use as bits
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits_invalid(block_object, bits_value)
    update_nonce(block_object)


def update_block_variables_with_an_invalid_nonce(block_object, nonce_value, conn, pay_address=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "nonce" value.

    :param nonce_value: The value to use as nonce
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce_invalid(block_object, nonce_value)


def update_block_variables_parent_block_data_to_provided_block(block_object, parent_block_hash, conn,
                                                               pay_address=None):
    """
    Initiates the VALID updating process for the block, setting "parent block data" variables to point to a provided
    block hash or to Genesis block.

    :param block_object: The block object that holds the variables to update
    :param parent_block_hash: accepts block hash as bytes or the string "genesis"
    """
    block_template = json_rpc_requests.get_block_template_request(conn=conn, pay_address=pay_address)['result']

    if parent_block_hash.lower() == "genesis":
        update_parent_blocks_data_to_genesis(block_object)
    else:
        update_parent_blocks_data_to_provided_block(block_object, parent_block_hash)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_version(block_object, version_int):
    """
    Updates the block object variable "version" using the provided int.

    :param version_int: The required version as an int
    :param block_object: The block object that holds the variables to update
    """
    version = bytes([version_int])
    block_object.version_bytes = version


def update_version_invalid(block_object):
    """
    Updates the block object variable "version" to an empty byte (b"").

    :param block_object: The block object that holds the variables to update
    """
    block_object.version_bytes = b""


def update_block_version(block_object, block_template):
    version_int = block_template['version']
    block_object.version_bytes = version_int.to_bytes(4, byteorder='little')


def update_parent_blocks_data(block_object, block_template):
    """
    Updates the block object variables "number of parent blocks" & "parent hashes" from the node.

    :param block_object: The block object that holds the variables to update
    """
    tip_hashes_list = block_template['parentHashes']

    # convert tips to bytes and flip
    reversed_tips_hashes_bytes = [(bytes.fromhex(tip))[::-1] for tip in tip_hashes_list]
    block_object.number_of_parent_blocks_bytes = (len(tip_hashes_list)).to_bytes(1, byteorder='little')
    block_object.parent_hashes = reversed_tips_hashes_bytes


def update_parent_blocks_data_to_genesis(block_object):
    """
    Updates the block object variables "number of parent blocks" & "parent hashes" to point Genesis block.

    :param block_object: The block object that holds the variables to update
    """
    tip_hashes_list = kaspad_constants.GENESIS_HASH
    tip_hashes_len_hex = hex(1).replace("0x", "").zfill(2)
    reversed_tips_hashes_bytes = general_utils.reverse_parent_hash_hex_to_bytes(tip_hashes_list)
    block_object.number_of_parent_blocks_bytes = bytes.fromhex(tip_hashes_len_hex)
    block_object.parent_hashes = reversed_tips_hashes_bytes


def update_parent_blocks_data_to_provided_block(block_object, parent_block_hash):
    """
    Updates blocks parents to the block hash/es provided.

    :param block_object: The block object that holds the variables to update
    :param parent_block_hash: The hash/es of the requested parent
    """

    if isinstance(parent_block_hash, list):
        tip_hashes_list = []
        for block_hash in parent_block_hash:
            hash_hex = block_hash.hex()
            tip_hashes_list.append(hash_hex)
    else:
        block_hash_hex = parent_block_hash.hex()
        tip_hashes_list = [block_hash_hex]
    tip_hashes_len_hex = hex(len(tip_hashes_list)).replace("0x", "").zfill(2)
    reversed_tips_hashes_bytes = general_utils.reverse_parent_hash_hex_to_bytes(tip_hashes_list)
    block_object.number_of_parent_blocks_bytes = bytes.fromhex(tip_hashes_len_hex)
    block_object.parent_hashes = reversed_tips_hashes_bytes


def update_hash_merkle_root(block_object, block_template):
    """
    Updates the block object variable "hash merkle root".

    :param block_object: The block object that holds the variable to update
    """
    # txs_list = block_object.get_block_txs_list_for_hash_merkle_root()
    txs_list = block_object.block_txs_list_as_bytes
    hash_merkle_root_bytes = calculate_hash_merkle_root(txs_list)
    block_object.hash_merkle_root_bytes = hash_merkle_root_bytes


def update_id_merkle_root(block_object, block_template):
    """
    Updates the block object variable "id merkle root" from the node.

    :param block_object: The block object that holds the variable to update
    """
    id_merkle_root_hex = block_template['acceptedIdMerkleRoot']
    reversed_id_merkle_root_bytes = (bytes.fromhex(id_merkle_root_hex))[::-1]
    block_object.id_merkle_root_bytes = reversed_id_merkle_root_bytes


def update_utxo_commitment(block_object, block_template):
    """
    Updates the block object variable "utxo commitment" from the node.

    :param block_object: The block object that holds the variable to update
    """
    utxo_commitment_hex = block_template["utxoCommitment"]
    reversed_utxo_commitment_bytes = (bytes.fromhex(utxo_commitment_hex))[::-1]
    block_object.utxo_commitment_bytes = reversed_utxo_commitment_bytes


def update_timestamp(block_object, block_template):
    """
    Updates the block object variable "timestamp" using current time.

    :param block_object: The block object that holds the variable to update
    """
    timestamp_int =time.time_ns()//1000000  # convert nanoseconds to miliseconds, as netsim works in miliseconds
    timestamp_bytes = timestamp_int.to_bytes(8, byteorder='little')
    block_object.timestamp_int = timestamp_int
    block_object.timestamp_bytes = timestamp_bytes


def update_timestamp_invalid(block_object, timestamp_value):
    """
    Updates the block object variable "timestamp" based on the received value.

    :param timestamp_value: The value to use as timestamp
    :param block_object: The block object that holds the variable to update
    """
    if type(timestamp_value) is int:
        updated_timestamp_int = (timestamp_value + (1 << 64)) % (1 << 64)
        updated_timestamp_temp = hex(updated_timestamp_int).replace("0x", "")
        reverse_updated_timestamp_temp = general_utils.reverse_hex(updated_timestamp_temp)
        updated_timestamp_bytes = general_utils.convert_hex_to_bytes(reverse_updated_timestamp_temp.ljust(16, "0"))
        block_object.timestamp_bytes = updated_timestamp_bytes
        block_object.timestamp_int = updated_timestamp_int
    elif timestamp_value is None:
        block_object.timestamp_bytes = b""
        block_object.timestamp_int = None
    else:
        # TODO - what's that ???
        timestamp_str = timestamp_value
        block_object.timestamp_bytes = bytes(timestamp_str, "utf-8")


def update_bits(block_object, block_template):
    """
    Updates the block object variable "bits" from the node.

    :param block_object: The block object that holds the variable to update
    """
    bits_bytes = (bytes.fromhex(block_template['bits']))[::-1]
    block_object.bits_bytes = bits_bytes


def update_bits_invalid(block_object, bits_value):
    """
    Updates the block object variable "bits" based on the received value.

    :param bits_value: The value to use as bits
    :param block_object: The block object that holds the variable to update
    """
    if type(bits_value) is int:
        updated_bits_temp_int = (bits_value + (1 << 64) % (1 << 64))
        updated_bits_temp_hex = hex(updated_bits_temp_int).replace("0x", "")
        reverse_updated_bits_temp = general_utils.reverse_hex(updated_bits_temp_hex)
        updated_bits_bytes = general_utils.convert_hex_to_bytes(reverse_updated_bits_temp.ljust(16, "0"))
        block_object.bits_bytes = updated_bits_bytes
    elif bits_value is None:
        block_object.bits_bytes = b''
    else:
        # TODO - whats that ???
        bits_str = bits_value
        block_object.bits_bytes = bytes(bits_str, "utf-8")


def update_nonce(block_object):
    """
    Updates the block object variable "nonce" based on the calculations required for find the correct block hash.

    :param block_object: The block object that holds the variable to update
    """
    # block_header_list = block_object.get_block_header_list()
    # nonce = calculate_nonce(block_header_list)
    nonce = calculate_nonce(block_object)
    block_object.nonce_bytes = nonce


def update_nonce_invalid(block_object, nonce_value):
    """
    Updates the block object variable "nonce" based on the received value.

    :param nonce_value: The value to use as nonce
    :param block_object: The block object that holds the variable to update
    """
    if type(nonce_value) is int:
        updated_nonce_temp = hex((nonce_value + (1 << 64)) % (1 << 64)).replace("0x", "")
        reverse_updated_nonce_temp = general_utils.reverse_hex(updated_nonce_temp)
        updated_nonce_bytes = general_utils.convert_hex_to_bytes(reverse_updated_nonce_temp.ljust(16, "0"))
        block_object.nonce_bytes = updated_nonce_bytes
    elif nonce_value is None:
        block_object.nonce_bytes = b""
    else:
        # TODO ????
        nonce_str = nonce_value
        block_object.nonce_bytes = bytes(nonce_str, "utf-8")


# ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

def update_all_txs(block_object, block_template, native_txs=None):
    """
    Updates all tsx data based on information received from the node and from local calculations.

    :param block_object: The block object that holds the variable to update
    """
    coinbase_tx_object = update_coinbase_tx(block_template)
    block_object.coinbase_tx_obj = coinbase_tx_object
    if native_txs == None:
        return
    for tx in native_txs:
        block_object.add_native_transaction(tx)


def update_coinbase_tx(block_template):
    """
    Creates a new coinbase_tx_object based on data received from the node (request get_block_template_request()).

    :return: new_coinbase_tx object
    """
    coinbase_tx_hex = block_template['transactions'][0]["data"]
    coinbase_tx_bytes = bytes.fromhex(coinbase_tx_hex)
    coinbase_tx_bytes_stream = BytesIO(coinbase_tx_bytes)
    new_coinbase_tx = Tx.parse_tx(coinbase_tx_bytes_stream)
    return new_coinbase_tx


def update_native_txs(tx_object):
    pass


# ========== Calculate Nonce method ========== #

def calculate_nonce(block_object):
    """
    Looks for a hash that will be smaller than the target.

    :param block_object: The block header bytes parsed as a list
    :return: New nonce as bytes
    """
    block_target = block_object.target_int
    target = min(block_target, kaspad_constants.MAX_BLOCK_TARGET)
    hash = block_object.block_header_hash
    block_object.nonce_int = random.randint(0, kaspad_constants.MAX_UINT64)

    while hash >= target:
        block_object.nonce_int = (block_object.nonce_int + 1) % kaspad_constants.MAX_UINT64
        hash = block_object.block_header_hash

    return block_object.nonce_bytes


# ========== Calculate Hash Merkle Root methods ========== #

def calculate_hash_merkle_root(txs_list):
    """
    Calculates the block hash merkle root from the received block_body_list

    :param txs_list: The list of all the block txs excluding the "payload length" & the "payload"
    :return: hash merkle root as bytes
    """
    txs_hashes_list = hash_txs(txs_list)
    # hash_merkle_root_hex = loop_through_txs_hashes_list(txs_hashes_list)
    hash_merkle_root = MerkleTree.merkle_root(txs_hashes_list)
    return hash_merkle_root


def hash_txs(txs_list):
    """
    Generates a hash for all txs that are received.

    :param txs_list: List of all txs in the block
    :return: List of txs hashes
    """
    txs_hashes_list = []
    for tx in txs_list:
        tx_hash = general_utils.hash_256(tx)
        txs_hashes_list.append(tx_hash)
    return txs_hashes_list
