"""
This module holds all the UPDATE methods for the automation project.
"""

import random
from io import BytesIO
import time
from kaspy_tools.kaspad import json_rpc_client
from kaspy_tools.kaspa_model.tx import Tx
from kaspy_tools.utils import general_utils


# ========== Update Block Methods ========== #

def update_all_valid_block_variables(block_object, block_template, conn=None):
    """
    Initiates the VALID updating process for the entire block

    :param block_object: The block object that holds the variables to update
    """

    update_parent_blocks_data(block_object,block_template)
    update_all_txs(block_object,block_template)
    update_hash_merkle_root(block_object,block_template)
    update_id_merkle_root(block_object,block_template)
    update_utxo_commitment(block_object,block_template)
    update_timestamp(block_object,block_template)
    update_bits(block_object,block_template)
    update_nonce(block_object)


def update_block_variables_using_invalid_version_data(block_object, version_int, url=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "version" value.

    :param version_int: The required version as an int
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)
    if version_int is None:
        update_version_invalid(block_object)
    else:
        update_version(block_object, version_int)


def update_block_variables_without_parent_block_data(block_object, url=None):
    """
    Initiates the VALID updating process for the block, ignoring "parent block data" variables

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_txs(block_object, url=None):
    """
    Initiates the VALID updating process for the block, ignoring "Txs" objects

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_hash_merkle_root(block_object, url=None):
    """
    Initiates the VALID updating process for the block, ignoring "hash merkle root" variable

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_id_merkle_root(block_object, url=None):
    """
    Initiates the VALID updating process for the block, ignoring "ID merkle root" variable

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_without_utxo_commitment(block_object, url=None):
    """
    Initiates the VALID updating process for the block, ignoring "utxo commitment" variable

    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_with_an_invalid_timestamp(block_object, timestamp_value, url=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "timestamp" value.

    :param timestamp_value: The value to use as the invalid timestamp
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp_invalid(block_object, timestamp_value)
    update_bits(block_object, block_template)
    update_nonce(block_object)


def update_block_variables_with_an_invalid_bits(block_object, bits_value, url=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "bits" value.

    :param bits_value: The value to use as bits
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits_invalid(block_object, bits_value)
    update_nonce(block_object)


def update_block_variables_with_an_invalid_nonce(block_object, nonce_value, url=None):
    """
    Initiates the VALID updating process for the block, adding an invalid "nonce" value.

    :param nonce_value: The value to use as nonce
    :param block_object: The block object that holds the variables to update
    """
    block_template = json_rpc_client.get_block_template(url)['result']

    update_parent_blocks_data(block_object, block_template)
    update_all_txs(block_object, block_template)
    update_hash_merkle_root(block_object, block_template)
    update_id_merkle_root(block_object, block_template)
    update_utxo_commitment(block_object, block_template)
    update_timestamp(block_object, block_template)
    update_bits(block_object, block_template)
    update_nonce_invalid(block_object, nonce_value)


def update_block_variables_parent_block_data_to_provided_block(block_object, parent_block_hash, url=None):
    """
    Initiates the VALID updating process for the block, setting "parent block data" variables to point to a provided
    block hash or to Genesis block.

    :param block_object: The block object that holds the variables to update
    :param parent_block_hash: accepts block hash as bytes or the string "genesis"
    """
    block_template = json_rpc_client.get_block_template(url)['result']

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
    block_object.set_version(version)


def update_version_invalid(block_object):
    """
    Updates the block object variable "version" to an empty byte (b"").

    :param block_object: The block object that holds the variables to update
    """
    block_object.set_version(b"")


def update_parent_blocks_data(block_object, block_template):
    """
    Updates the block object variables "number of parent blocks" & "parent hashes" from the node.

    :param block_object: The block object that holds the variables to update
    """
    tip_hashes_list = block_template['parentHashes']

    #convert tips to bytes and flip
    reversed_tips_hashes_bytes = [ (bytes.fromhex(tip))[::-1]  for tip in tip_hashes_list ]
    block_object.set_number_of_parent_blocks((len(tip_hashes_list)).to_bytes(1,byteorder='little'))
    block_object.set_parent_hashes(reversed_tips_hashes_bytes)


def update_parent_blocks_data_to_genesis(block_object):
    """
    Updates the block object variables "number of parent blocks" & "parent hashes" to point Genesis block.

    :param block_object: The block object that holds the variables to update
    """
    tip_hashes_list = json_rpc_client.get_genesis_blockhash_from_constants()
    tip_hashes_len_hex = hex(1).replace("0x", "").zfill(2)
    reversed_tips_hashes_bytes = general_utils.reverse_parent_hash_hex_to_bytes(tip_hashes_list)
    block_object.set_number_of_parent_blocks(bytes.fromhex(tip_hashes_len_hex))
    block_object.set_parent_hashes(reversed_tips_hashes_bytes)


def update_parent_blocks_data_to_provided_block(block_object, parent_block_hash):
    """
    Updates blocks parents to the block hash/es provided.

    :param block_object: The block object that holds the variables to update
    :param parent_block_hash: The hash/es of the requested parent
    """

    if isinstance(parent_block_hash, list):
        tip_hashes_list = []
        for block_hash in parent_block_hash:
            hash_hex = general_utils.convert_bytes_to_hex(block_hash)
            tip_hashes_list.append(hash_hex)
    else:
        block_hash_hex = general_utils.convert_bytes_to_hex(parent_block_hash)
        tip_hashes_list = [block_hash_hex]
    tip_hashes_len_hex = hex(len(tip_hashes_list)).replace("0x", "").zfill(2)
    reversed_tips_hashes_bytes = general_utils.reverse_parent_hash_hex_to_bytes(tip_hashes_list)
    block_object.set_number_of_parent_blocks(bytes.fromhex(tip_hashes_len_hex))
    block_object.set_parent_hashes(reversed_tips_hashes_bytes)


def update_hash_merkle_root(block_object, block_template):
    """
    Updates the block object variable "hash merkle root".

    :param block_object: The block object that holds the variable to update
    """
    txs_list = block_object.get_block_txs_list_for_hash_merkle_root()
    hash_merkle_root = calculate_hash_merkle_root(txs_list)
    block_object.set_hash_merkle_root(hash_merkle_root)


def update_id_merkle_root(block_object, block_template):
    """
    Updates the block object variable "id merkle root" from the node.

    :param block_object: The block object that holds the variable to update
    """
    id_merkle_root = block_template['acceptedIdMerkleRoot']
    reversed_id_merkle_root = (bytes.fromhex(id_merkle_root))[::-1]
    block_object.set_id_merkle_root(reversed_id_merkle_root)


def update_utxo_commitment(block_object, block_template):
    """
    Updates the block object variable "utxo commitment" from the node.

    :param block_object: The block object that holds the variable to update
    """
    utxo_commitment = block_template["utxoCommitment"]
    reversed_utxo_commitment = (bytes.fromhex(utxo_commitment))[::-1]
    block_object.set_utxo_commitment(reversed_utxo_commitment)


def update_timestamp(block_object, block_template):
    """
    Updates the block object variable "timestamp" using current time.

    :param block_object: The block object that holds the variable to update
    """
    timestamp_int = int(time.time())
    timestamp_bytes = timestamp_int.to_bytes(8, byteorder='little')
    block_object.set_timestamp(timestamp_bytes)


def update_timestamp_invalid(block_object, timestamp_value):
    """
    Updates the block object variable "timestamp" based on the received value.

    :param timestamp_value: The value to use as timestamp
    :param block_object: The block object that holds the variable to update
    """
    if type(timestamp_value) is int:
        updated_timestamp_temp = hex((timestamp_value + (1 << 64)) % (1 << 64)).replace("0x", "")
        reverse_updated_timestamp_temp = general_utils.reverse_hex(updated_timestamp_temp)
        updated_timestamp_bytes = general_utils.convert_hex_to_bytes(reverse_updated_timestamp_temp.ljust(16, "0"))
        block_object.set_timestamp(updated_timestamp_bytes)
    elif timestamp_value is None:
        block_object.set_timestamp(b"")
    else:
        timestamp_str = timestamp_value
        block_object.set_timestamp(bytes(timestamp_str, "utf-8"))


def update_bits(block_object, block_template):
    """
    Updates the block object variable "bits" from the node.

    :param block_object: The block object that holds the variable to update
    """
    # bits = json_rpc_client.get_node_bits()
    # bits_bytes = general_utils.convert_hex_to_bytes(bits)
    # reversed_bits = general_utils.reverse_bytes(bits_bytes)
    bits_bytes = (bytes.fromhex(block_template['bits']))[::-1]
    block_object.set_bits(bits_bytes)


def update_bits_invalid(block_object, bits_value):
    """
    Updates the block object variable "bits" based on the received value.

    :param bits_value: The value to use as bits
    :param block_object: The block object that holds the variable to update
    """
    if type(bits_value) is int:
        updated_bits_temp = hex((bits_value + (1 << 64)) % (1 << 64)).replace("0x", "")
        reverse_updated_bits_temp = general_utils.reverse_hex(updated_bits_temp)
        updated_bits_bytes = general_utils.convert_hex_to_bytes(reverse_updated_bits_temp.ljust(16, "0"))
        block_object.set_timestamp(updated_bits_bytes)
    elif bits_value is None:
        block_object.set_bits(b"")
    else:
        bits_str = bits_value
        block_object.set_timestamp(bytes(bits_str, "utf-8"))


def update_nonce(block_object):
    """
    Updates the block object variable "nonce" based on the calculations required for find the correct block hash.

    :param block_object: The block object that holds the variable to update
    """
    block_header_list = block_object.get_block_header_list()
    nonce = calculate_nonce(block_header_list)
    block_object.set_nonce(nonce)


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
        block_object.set_timestamp(updated_nonce_bytes)
    elif nonce_value is None:
        block_object.set_nonce(b"")
    else:
        nonce_str = nonce_value
        block_object.set_timestamp(bytes(nonce_str, "utf-8"))


# ========== Update Tx Methods ========== #  >>>>>>>> NEEDS MORE WORK!!!

def update_all_txs(block_object, block_template):
    """
    Updates all tsx data based on information received from the node and from local calculations.

    :param block_object: The block object that holds the variable to update
    """
    coinbase_tx_object = update_coinbase_tx(block_template)
    block_object.set_coinbase_tx(coinbase_tx_object)


def update_num_of_txs_in_block(tx_object):
    pass


def update_coinbase_tx(block_template):
    """
    Creates a new coinbase_tx_object based on data received from the node (request get_block_template_request()).

    :return: new_coinbase_tx object
    """
    coinbase_tx_hex = block_template["coinbaseTxn"]["data"]
    coinbase_tx_bytes = bytes.fromhex(coinbase_tx_hex)
    coinbase_tx_bytes_stream = BytesIO(coinbase_tx_bytes)
    new_coinbase_tx = Tx.parse_tx(coinbase_tx_bytes_stream)
    return new_coinbase_tx


def update_native_txs(tx_object):
    pass


# ========== Calculate Nonce method ========== #


def calculate_nonce(block_header_list):
    """
    Looks for a hash that will be smaller than the target.

    :param block_header_list: The block header bytes parsed as a list
    :return: New nonce as bytes
    """
    block_header_list = block_header_list
    block_header = general_utils.build_element_from_list(block_header_list)
    bits = block_header_list[-2]
    original_nonce = block_header_list[-1]
    nonce = block_header_list[-1]
    while True:  # Runs until a nonce smaller than Target is found
        nonce_int = int.from_bytes(nonce, "little")
        exponent = bits[-1]
        coefficient = int.from_bytes(bits[:-1], "little")
        target = coefficient * 256 ** (exponent - 3)
        # print("target: " + str(target))
        block_hash = int.from_bytes(general_utils.hash_256(block_header), "little")
        # print("block_hash: " + str(block_hash))

        if block_hash >= target:
            # If nonce == original nonce or nonce_int > than MAX_UINT64 generate a random nonce
            if nonce == original_nonce or nonce_int > json_rpc_client.get_max_uint64_from_constants():
                nonce_int = random.randint(0, json_rpc_client.get_max_uint64_from_constants())
                nonce_hex = hex(nonce_int).replace("0x", "").zfill(16)
                nonce = general_utils.convert_hex_to_bytes(nonce_hex)
            else:
                nonce_int += 1
                nonce_hex = hex(nonce_int).replace("0x", "").zfill(16)
                nonce = general_utils.convert_hex_to_bytes(nonce_hex)

            block_header_list[-1] = nonce
            block_header = general_utils.build_element_from_list(block_header_list)
        else:
            return nonce


# ========== Calculate Hash Merkle Root methods ========== #

def calculate_hash_merkle_root(txs_list):
    """
    Calculates the block hash merkle root from the received block_body_list

    :param txs_list: The list of all the block txs excluding the "payload length" & the "payload"
    :return: hash merkle root as bytes
    """
    txs_hashes_list = hash_txs(txs_list)
    hash_merkle_root_hex = loop_through_txs_hashes_list(txs_hashes_list)
    return hash_merkle_root_hex


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


def loop_through_txs_hashes_list(txs_hashes_list):
    """
    Loops through the txs hashes list until it find the hash merkle root

    :param txs_hashes_list: List of the hashes for all txs in the block
    :return: Hash merkle root as bytes array
    """
    original_list = txs_hashes_list
    new_list = []

    if len(original_list) == 1:
        hash_merkle_root = original_list[0]
        # reversed_hash_merkle_root = general_utils.reverse_bytes(hash_merkle_root)
        return hash_merkle_root

    if len(original_list) > 1 and len(original_list) % 2 != 0:
        last_tx_hash = original_list[-1]
        original_list.append(last_tx_hash)

    if len(original_list) > 1 and len(original_list) % 2 == 0:
        for i in range(0, len(original_list), 2):
            hash1 = original_list[i]
            hash2 = original_list[i + 1]
            combined_hashes_bytes = hash1 + hash2
            new_hash_bytes = general_utils.hash_256(combined_hashes_bytes)
            new_list.append(new_hash_bytes)

    hash_merkle_root = loop_through_txs_hashes_list(new_list)
    return hash_merkle_root
