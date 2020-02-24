"""
This module holds the methods that handle all the JSON RPC requests for the automation project.
"""

from utils import general_utils
import KOSMOS
from KOSMOS.JSON_RPC import block_generator, json_rpc_requests, json_rpc_node
import logging
from model.tx_out import TxOut

local_logger = KOSMOS.logs.config_logger.get_local_logger(__name__)


def submit_valid_block(block_file_path, options=None):
    """
    Builds and submit a valid block based on the file path and subnetwork options that were provided to the DAG-block network.
    Returns the action's response parsed by the "error_handler" method as well as the block hash as a hex string.

    :param block_file_path: The path of the block binary file
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :return: Action_status of the submit request & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_valid_block_and_hash(block_file_path)
    block_hex, block_hash_hex = convert_block_data_for_rpc_request(block_bytes, block_hash)
    response = json_rpc_requests.submit_block_request(block_hex, options)
    action_status = error_handler(response["error"])
    return action_status, block_hash_hex


def submit_pre_generated_block(block_bytes, block_hash, options=None):
    """
    Submit a block that was previously generated.
    Returns the action's response parsed by the "error_handler" method as well as the block hash as a hex string.

    :param block_bytes: The block bytes array
    :param block_hash: The block hash as bytes
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :return: Action_status of the submit request & block_hash_hex
    """
    block_hex, block_hash_hex = convert_block_data_for_rpc_request(block_bytes, block_hash)
    response = json_rpc_requests.submit_block_request(block_hex, options)
    action_status = error_handler(response["error"])
    return action_status, block_hash_hex


def submit_blocks_from_binary_file(block_file_path):
    """
    Submit blocks from a provided file path.
    Blocks must be in Hex format.

    :param block_file_path: The path for the requested file
    """
    file = open(block_file_path, "r")
    counter = 1
    while True:
        block_hex = file.readline()[:-1]
        if block_hex == "":
            break
        response = json_rpc_requests.submit_block_request(block_hex)
        action_status = error_handler(response["error"])
        local_logger.debug(print("block " + str(counter) + " " + action_status))
        counter += 1
    file.close()
    print("All blocks in file were submitted successfully")


def submit_block_with_specific_parents(block_file_path, parent_block_hash, options=None):
    """
    Builds and submit a block that points to a specific parent block, either using the provided hash/es or using
    the "Genesis" block.

    :param block_file_path: The path of the block binary file
    :param parent_block_hash: Accepts a block hash as bytes or the string "genesis"
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :return: Action_status of the submit request & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_block_to_specific_parent(block_file_path, parent_block_hash)
    block_hex = general_utils.convert_bytes_to_hex(block_bytes)
    block_hash_hex = general_utils.convert_bytes_to_hex(block_hash)
    response = json_rpc_requests.submit_block_request(block_hex, options)
    action_status = error_handler(response["error"])
    return action_status, block_hash_hex


def submit_modified_block(block_file_path, invalid_parameter_string, invalid_arg_type=None, options=None):
    """
    Builds and submit an invalid block based on the file path and subnetwork options that were provided to the DAG-block network.
    Returns the action's response parsed by the "error_handler" method as well as the block hash as a hex string.


    :param invalid_parameter_string: The parameter that is to be invalid for the testing purpose.
                                     This arg accepts the following strings only:
                                     "parent_block_data", "txs", "_hash_merkle_root", "_id_merkle_root", "_utxo_commitment",
                                     "_timestamp", "_bits", "_nonce"
    :param block_file_path: The path of the block binary file
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :param invalid_arg_type: The required invalid arg type for the test.
                            Use one of the following options or leave as None:
                            int = any integer
                            str = any string
    :return: Action_status of the submit request & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_modified_block_and_hash(block_file_path,
                                                                               invalid_parameter_string,
                                                                               invalid_arg_type)
    block_hex = general_utils.convert_bytes_to_hex(block_bytes)
    block_hash_hex = general_utils.convert_bytes_to_hex(block_hash)
    response = json_rpc_requests.submit_block_request(block_hex, options)
    action_status = error_handler(response["error"])
    return action_status, block_hash_hex


def convert_block_data_for_rpc_request(block_bytes, block_hash):
    """
    Convert block data from bytes to hex as required for the RPC requests.

    :param block_bytes: The block bytes array
    :param block_hash: The block hash as bytes
    :return: block_hex and block_hash_hex
    """
    block_hex = general_utils.convert_bytes_to_hex(block_bytes)
    block_hash_hex = general_utils.convert_bytes_to_hex(block_hash)
    return block_hex, block_hash_hex


def error_handler(response_error):
    """
    Verify if an error was received in the block action that was conducted.

    :param response_error: The "error" dictionary that is part of the block cmd response formatted as: response["error"]
    :return: String, in case error was received, the code and message in one string, else "No error" string
    """
    if response_error is not None:
        error = "Error Code: " + str(response_error["code"]) + ", Error Message: " + str(response_error["message"])
        return error
    else:
        message = "No error"
        return message


def get_current_tip_hashes():
    """
    Returns the current tips hashes using the function in json_rpc_node.py.

    :return: The tips hashes as a list
    """
    return json_rpc_node.get_node_tip_hashes_list()


def get_block_data(block_hash):
    """
    Returns the requested block data status using the function in json_rpc_node.py.

    :param block_hash: Hash of the requested block
    :return: block data status as a string
    """
    return json_rpc_node.get_block_data_status(block_hash)


def get_blocks(url, block_count):
    raw_blocks, verbose_blocks = json_rpc_requests.get_blocks(url, block_count)
    return raw_blocks, verbose_blocks
