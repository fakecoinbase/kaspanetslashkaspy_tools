"""
This module holds the methods that handle all the JSON RPC requests for the automation project.
"""
from kaspy_tools.kaspad.json_rpc import json_rpc_requests, json_rpc_node
from kaspy_tools.kaspad import kaspad_constants


def submit_block_request(block_hex, options=None):
    return json_rpc_requests.submit_block_request(block_hex, options)

def submit_raw_transaction_request(tx_hex, options=None):
    return json_rpc_requests.submit_raw_tx(tx_hex, options)


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
    """
    Returns the the requested amount of blocks from the Node URL that was provided.
    using the function in json_rpc_node.py.

    :param url: The URL of the Node
    :param block_count: The amount of blocks to retrieve
    :return: block data as raw_blocks, verbose_blocks
    """
    raw_blocks, verbose_blocks = json_rpc_requests.get_blocks(url, block_count)
    return raw_blocks, verbose_blocks


def get_block_template():
    res = json_rpc_requests.get_block_template_request()
    return res

def get_genesis_blockhash_from_constants():
    """
    Returns the blockhash value of the genesis block from json_rpc_constants.py as a list.
    """
    return [kaspad_constants.GENESIS_HASH]


def get_node_id_merkle_root():
    """
    Returns the current node id merkle root using the function in json_rpc_node.py.
    """
    return json_rpc_node.get_node_id_merkle_root()


def get_node_utxo_commitment():
    """
    Returns the current node id utxo commitment using the function in json_rpc_node.py.
    """
    return json_rpc_node.get_node_utxo_commitment()


def get_node_bits():
    """
    Returns the current node bits using the function in json_rpc_node.py.
    """
    return json_rpc_node.get_node_bits()


def get_coinbase_tx_data():
    """
    Returns the current node coinbase tx data using the function in json_rpc_node.py.
    """
    return json_rpc_node.get_coinbase_tx_data()


def get_max_uint64_from_constants():
    """
    Returns the max_uint64 value from json_rpc_constants.py.
    """
    return kaspad_constants.MAX_UINT64


def get_block_dag_num_of_blocks():
    """
    Return current amount of blocks from the node using the function in json_rpc_node.py.
    """
    return json_rpc_node.get_block_dag_num_of_blocks()