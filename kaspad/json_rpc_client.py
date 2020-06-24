"""
This module holds the methods that handle all the JSON RPC requests for the automation project.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.kaspad import kaspad_constants

KT_logger = config_logger.get_kaspy_tools_logger()

def submit_block_request(*, block_hex, options=None, conn=None):
    return json_rpc_requests.submit_block_request(block_hex, options, conn=conn)

def submit_raw_transaction_request(tx_hex, options=None, conn=None):
    return json_rpc_requests.submit_raw_tx(tx_hex, options, conn)


def get_current_tip_hashes(conn=None):
    """
    Returns the current tips hashes.

    :return: The tips hashes as a list
    """
    # return json_rpc_node.get_node_tip_hashes_list(conn)
    response = json_rpc_requests.get_block_dag_info_request(conn)
    tip_hash_list = response["result"]["tipHashes"]
    return tip_hash_list


# def get_block_data(block_hash, conn=None):
#     """
#     Returns the requested block data status
#
#     :param block_hash: Hash of the requested block
#     :return: block data status as a string
#     """
#     return json_rpc_node.get_block_data_status(block_hash, conn)


def get_blocks(block_count, conn=None):
    """
    Returns the the requested amount of blocks from the Node URL that was provided.

    :param url: The URL of the Node
    :param block_count: The amount of blocks to retrieve
    :return: block data as raw_blocks, verbose_blocks
    """
    raw_blocks, verbose_blocks = json_rpc_requests.get_blocks(block_count, conn=conn)
    return raw_blocks, verbose_blocks


# def get_block_template(conn=None, pay_address=None):
#     res = json_rpc_requests.get_block_template_request(conn=conn, payAddress=pay_address)


    return res

# def get_genesis_blockhash_from_constants():
#     """
#     Returns the blockhash value of the genesis block.
#     """
#     return [kaspad_constants.GENESIS_HASH]


# def get_node_id_merkle_root(conn=None):
#     """
#     Returns the current node id merkle root
#     """
#     return json_rpc_node.get_node_id_merkle_root(conn)


# def get_node_utxo_commitment(conn=None):
#     """
#     Returns the current node id utxo commitment
#     """
#     return json_rpc_node.get_node_utxo_commitment(conn)


# def get_node_bits(conn=None):
#     """
#     Returns the current node bits
#     """
#     return json_rpc_node.get_node_bits(conn)


# def get_coinbase_tx_data(conn=None):
#     """
#     Returns the current node coinbase tx data
#     """
#     return json_rpc_node.get_coinbase_tx_data(conn)
#

def get_max_uint64_from_constants():
    """
    Returns the max_uint64 value.
    """
    return kaspad_constants.MAX_UINT64


def get_block_dag_num_of_blocks(conn=None):
    """
    Return current amount of blocks from the node
    """
    # return json_rpc_node.get_block_dag_num_of_blocks(conn)
    response = json_rpc_requests.get_block_dag_info_request(url)
    num_of_blocks = response["result"]["blocks"]
    return num_of_blocks



def get_peer_info(conn=None):
    info = json_rpc_requests.get_peer_info_request(conn)
    return info
