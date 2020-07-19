"""
This module holds the methods that handle all the kaspa-d block utils for the automation project.
"""
from kaspy_tools.kaspad.utilities import block_generator
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.logs import config_logger
from kaspy_tools.utils import general_utils

KT_logger = config_logger.get_kaspy_tools_logger()


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


def submit_valid_block(*, conn=None, native_txs=None, netprefix='kaspadev'):
    """
    Builds and submit a valid block based on a block template.
    Returns the action's response parsed by the "error_handler" method
    as well as the block hash as a hex string.

    :return: The original response of the submit request, response_json & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_valid_block_from_template(conn=conn, native_txs=native_txs,
                                                                                 netprefix=netprefix)

    response, response_json = json_rpc_requests.submit_block_request(hex_block=block_bytes.hex(), conn=conn)
    return response, response_json, block_hash.hex()


def submit_pre_generated_block(block_bytes, block_hash, options=None, conn=None):
    """
    Submit a block that was previously generated.
    Returns the action's response parsed by the "error_handler" method as well as the block hash as a hex string.

    :param block_bytes: The block bytes array
    :param block_hash: The block hash as bytes
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :return: The original response of the submit request, response_json & block_hash_hex
    """
    block_hex, block_hash_hex = convert_block_data_for_rpc_request(block_bytes, block_hash)
    response, response_json = json_rpc_requests.submit_block_request(hex_block=block_hex, options=options, conn=conn)
    return response, response_json, block_hash_hex


def submit_block_with_specific_parents(*, parent_block_hash, options=None, conn=None):
    """
    Builds and submit a block that points to a specific parent block, either using the provided hash/es or using
    the "Genesis" block.

    :param parent_block_hash: Accepts a block hash as bytes or the string "genesis"
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :return: The original response of the submit request, response_json & block_hash_hex
    """
    block_bytes, block_hash_hex = block_generator.generate_block_to_specific_parent(parent_block_hash, conn=conn)
    block_hex = block_bytes.hex()
    response, response_json = json_rpc_requests.submit_block_request(hex_block=block_hex, options=options, conn=conn)
    return response, response_json, block_hash_hex, block_bytes


def submit_modified_block(*, invalid_parameter_string, invalid_arg_type=None,
                          options=None, netprefix='kaspadev', conn=None):
    """
    Builds and submit an invalid block based on the file path and subnetwork options that were provided to the DAG-block network.
    Returns the action's response parsed by the "error_handler" method as well as the block hash as a hex string.


    :param invalid_parameter_string: The parameter that is to be invalid for the testing purpose.
                                     This arg accepts the following strings only:
                                     "parent_block_data", "txs", "_hash_merkle_root", "_id_merkle_root", "_utxo_commitment",
                                     "_timestamp", "_bits", "_nonce"
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :param invalid_arg_type: The required invalid arg type for the test.
                            Use one of the following options or leave as None:
                            int = any integer
                            str = any string
    :return: The original response of the submit request, response_json & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_modified_block_and_hash(variable_str=invalid_parameter_string,
                                                                               invalid_arg_type=invalid_arg_type,
                                                                               netprefix=netprefix,
                                                                               conn=conn)
    block_hex = block_bytes.hex()
    block_hash_hex = block_hash.hex()
    response, response_json = json_rpc_requests.submit_block_request(hex_block=block_hex, options=options, conn=conn)
    return response, response_json, block_hash_hex


def convert_block_data_for_rpc_request(block_bytes, block_hash):
    """
    Convert block data from bytes to hex as required for the RPC requests.

    :param block_bytes: The block bytes array
    :param block_hash: The block hash as bytes
    :return: block_hex and block_hash_hex
    """
    block_hex = block_bytes.hex()
    if type(block_hash) is bytes:
        block_hash_hex = block_hash.hex()
    else:
        block_hash_hex = block_hash
    return block_hex, block_hash_hex


def get_current_tip_hashes(conn=None):
    """
    Returns the current tips hashes using the function in json_rpc_requests.py.

    :return: The tips hashes as a list
    """
    response = json_rpc_requests.get_block_dag_info_request(conn)
    return response["result"]["tipHashes"]


def get_blocks(block_count, conn=None):
    """
    Returns the the requested amount of blocks from the Node URL that was provided.
    using the function in json_rpc_requests.py.

    :param url: The URL of the Node
    :param block_count: The amount of blocks to retrieve
    :return: block data as raw_blocks, verbose_blocks
    """
    raw_blocks, verbose_blocks = json_rpc_requests.get_blocks(block_count, conn=conn)
    return raw_blocks, verbose_blocks


def get_block_dag_num_of_blocks(conn=None):
    """
    Return current amount of blocks from the node using the function in json_rpc_requests.py.
    """
    response = json_rpc_requests.get_block_dag_info_request(conn=conn)
    return response["result"]["blocks"]


def generate_valid_block_and_hash(conn=None):
    """
    Returns a valid block that was not submitted using the function in block_generator.py.
    """
    # return block_generator.generate_valid_block_and_hash(block_path, conn)
    return block_generator.generate_valid_block_from_template(conn=conn)
