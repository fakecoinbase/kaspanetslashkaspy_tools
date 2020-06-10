"""
This module holds the methods that handle the process of generating valid and invalid blocks for the automation project.
"""

from kaspy_tools.kaspa_model.block import Block
from kaspy_tools.utils import general_utils
from kaspy_tools.kaspad.utilities import updater
from kaspy_tools.kaspad import json_rpc_client
from kaspy_tools.kaspad.json_rpc import json_rpc_requests


# ========== Block generator methods ========== #

def generate_valid_block_from_template(*, conn=None, native_txs=None):
    new_block=Block.block_factory()
    block_template = json_rpc_client.get_block_template(conn=conn)['result']
    updater.update_all_valid_block_variables(new_block, block_template, conn=conn,  native_txs=native_txs)
    block_header = new_block.block_header_bytes
    block_hash = general_utils.hash_256(block_header)
    reversed_block_hash = general_utils.reverse_bytes(block_hash)
    block_body = new_block.get_block_body_bytes_array()
    valid_block = Block.rebuild_block(block_header, block_body)
    return valid_block, reversed_block_hash


# def generate_valid_block_and_hash(block_file_path, conn=None):
#     """
#     Generates a valid blue block using a provided block binary data from the blocks cartridge with updated data from the node
#     and local calculations.
#
#     :param block_file_path: The path of the block binary file
#     :return: Valid new block object & & block hash
#     """
#     block_bytes = general_utils.load_binary_file(block_file_path)
#     new_block = Block.parse_block(block_bytes)
#     block_template = json_rpc_client.get_block_template(conn=conn)['result']
#     updater.update_all_valid_block_variables(new_block, block_template, conn)
#     block_header = new_block.block_header_bytes
#     block_hash = general_utils.hash_256(block_header)
#     reversed_block_hash = general_utils.reverse_bytes(block_hash)
#     block_body = new_block.get_block_body_bytes_array()
#     valid_block = Block.rebuild_block(block_header, block_body)
#     return valid_block, reversed_block_hash


def generate_modified_block_and_hash(*, variable_str, options=None, invalid_arg_type=None, conn=None):
    """
    Generates an invalid block using a provided block binary data from the blocks cartridge with specifically updated
    data from the node and local calculations.

    :param variable_str: Accepts the following strings only:
                        "version, "parent_block_data", "txs", "hash_merkle_root", "id_merkle_root", "utxo_commitment",
                        "timestamp", "bits", "nonce"
    :param invalid_arg_type: The required invalid arg type for the test accepts the following options:
                            int = any integer
                            str = any string
                            None = None
    :return: Invalid new block object & block hash
    """
    # block_bytes = general_utils.load_binary_file(block_file_path)
    # new_block = Block.parse_block(block_bytes)
    new_block=Block.block_factory()
    variables_list = ["version", "parent_block_data", "txs", "hash_merkle_root", "id_merkle_root", "utxo_commitment", "timestamp",
                      "bits", "nonce"]
    if variable_str.lower() not in variables_list:
        print("Incorrect variable string provided: " + variable_str)
        print("module: block_generator.py, line: 48")
        raise SystemExit
    else:
        if variable_str.lower() == variables_list[0]:
            updater.update_block_variables_using_invalid_version_data(new_block, options, conn=conn)
        elif variable_str.lower() == variables_list[1]:
            updater.update_block_variables_without_parent_block_data(new_block, conn=conn)
        elif variable_str.lower() == variables_list[2]:
            updater.update_block_variables_without_txs(new_block, conn=conn)
        elif variable_str.lower() == variables_list[3]:
            updater.update_block_variables_without_hash_merkle_root(new_block, conn=conn)
        elif variable_str.lower() == variables_list[4]:
            updater.update_block_variables_without_id_merkle_root(new_block, conn=conn)
        elif variable_str.lower() == variables_list[5]:
            updater.update_block_variables_without_utxo_commitment(new_block, conn=conn)
        elif variable_str.lower() == variables_list[6]:
            updater.update_block_variables_with_an_invalid_timestamp(new_block, options, conn=conn)
        elif variable_str.lower() == variables_list[7]:
            updater.update_block_variables_with_an_invalid_bits(new_block, invalid_arg_type, conn=conn)
        elif variable_str.lower() == variables_list[8]:
            updater.update_block_variables_with_an_invalid_nonce(new_block, options, conn=conn)
    # block_header = new_block.get_block_header_bytes_array()
    # block_body = new_block.get_block_body_bytes_array()
    # invalid_block = Block.rebuild_block(block_header, block_body)
    # block_hash = general_utils.hash_256(block_header)
    # reversed_block_hash = general_utils.reverse_bytes(block_hash)

    # block_header = new_block.block_header_bytes()
    # block_body = new_block.get_block_body_bytes_array()
    # invalid_block = block_header + block_body
    # return invalid_block, reversed_block_hash
    new_block_bytes = bytes(new_block)
    new_block_hash = new_block.block_header_hash_bytes
    return new_block_bytes, new_block_hash


def generate_block_to_specific_parent(block_file_path, parent_block_hash, conn=None):
    """
    Generates a block while directing it to a specific set of tips or directly to the "Genesis" block.

    :param block_file_path: The path of the block binary file
    :param parent_block_hash: Accepts a block hash as bytes or the str "genesis"
    :return: New block object & block hash
    """
    # block_bytes = general_utils.load_binary_file(block_file_path)
    # new_block = Block.parse_block(block_bytes)
    new_block=Block.block_factory()
    updater.update_block_variables_parent_block_data_to_provided_block(new_block, parent_block_hash, conn=conn)
    modified_block = bytes(new_block)
    block_hash = new_block.block_header_hash_bytes.hex()
    return modified_block, block_hash
