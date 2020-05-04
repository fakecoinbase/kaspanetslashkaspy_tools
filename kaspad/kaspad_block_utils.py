"""
This module holds the methods that handle all the kaspa-d block utils for the automation project.
"""
from kaspy_tools.kaspad.utilities import block_generator
from kaspy_tools.kaspad import json_rpc_client
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


def submit_valid_block(*, conn=None, native_txs=None):
    """
    Builds and submit a valid block based on a block template.
    Returns the action's response parsed by the "error_handler" method
    as well as the block hash as a hex string.

    :return: The original response of the submit request, response_json & block_hash_hex
    """
    # block_bytes, block_hash = block_generator.generate_valid_block_and_hash(block_file_path, conn)
    block_bytes, block_hash = block_generator.generate_valid_block_from_template(conn=conn, native_txs=native_txs)

    block_hex, block_hash_hex = convert_block_data_for_rpc_request(block_bytes, block_hash)
    response, response_json = json_rpc_client.submit_block_request(block_hex=block_hex, conn=conn)
    return response, response_json, block_hash_hex


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
    response, response_json = json_rpc_client.submit_block_request(block_hex, options, conn)
    return response, response_json, block_hash_hex


def submit_blocks_from_binary_file(block_file_path, conn=None):
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
        response, response_json = json_rpc_client.submit_block_request(block_hex, conn)
        action_status = error_handler(response_json["error"])
        # local_logger.debug(print("block " + str(counter) + " " + action_status))
        counter += 1
    file.close()
    print("All blocks in file were submitted successfully")


def submit_block_with_specific_parents(block_file_path, parent_block_hash, options=None, conn=None):
    """
    Builds and submit a block that points to a specific parent block, either using the provided hash/es or using
    the "Genesis" block.

    :param block_file_path: The path of the block binary file
    :param parent_block_hash: Accepts a block hash as bytes or the string "genesis"
    :param options: Enter specific options that are required, for example: like a sub-network, else leave as None
    :return: The original response of the submit request, response_json & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_block_to_specific_parent(block_file_path,
                                                                                parent_block_hash, conn)
    block_hex = general_utils.convert_bytes_to_hex(block_bytes)
    block_hash_hex = general_utils.convert_bytes_to_hex(block_hash)
    response, response_json = json_rpc_client.submit_block_request(block_hex, options, conn)
    return response, response_json, block_hash_hex


def submit_modified_block(block_file_path, invalid_parameter_string, invalid_arg_type=None,
                          options=None, conn=None):
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
    :return: The original response of the submit request, response_json & block_hash_hex
    """
    block_bytes, block_hash = block_generator.generate_modified_block_and_hash(block_file_path,
                                                                               invalid_parameter_string,
                                                                               invalid_arg_type)
    block_hex = general_utils.convert_bytes_to_hex(block_bytes)
    block_hash_hex = general_utils.convert_bytes_to_hex(block_hash)
    response, response_json = json_rpc_client.submit_block_request(block_hex, options, conn)
    return response, response_json, block_hash_hex


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


def get_current_tip_hashes(conn=None):
    """
    Returns the current tips hashes using the function in json_rpc_client.py.

    :return: The tips hashes as a list
    """
    return json_rpc_client.get_current_tip_hashes(conn)


def get_block_data(block_hash, conn=None):
    """
    Returns the requested block data status using the function in json_rpc_client.py.

    :param block_hash: Hash of the requested block
    :return: block data status as a string
    """
    return json_rpc_client.get_block_data(block_hash, conn=None)


def get_blocks(block_count, conn=None):
    """
    Returns the the requested amount of blocks from the Node URL that was provided.
    using the function in json_rpc_client.py.

    :param url: The URL of the Node
    :param block_count: The amount of blocks to retrieve
    :return: block data as raw_blocks, verbose_blocks
    """
    raw_blocks, verbose_blocks = json_rpc_client.get_blocks(block_count, conn=conn)
    return raw_blocks, verbose_blocks


def get_block_dag_num_of_blocks(conn=None):
    """
    Return current amount of blocks from the node using the function in json_rpc_client.py.
    """
    return json_rpc_client.get_block_dag_num_of_blocks(conn)


def generate_valid_block_and_hash(block_path, conn=None):
    """
    Returns a valid block that was not submitted using the function in block_generator.py.
    """
    # return block_generator.generate_valid_block_and_hash(block_path, conn)
    return block_generator.generate_valid_block_from_template(conn=conn)
