"""
This module holds the methods that receive and parse specific data from the NODE for the automation project.
"""
import kaspy_tools.kaspad.kaspad_block_utils
from kaspy_tools.kaspad.json_rpc import json_rpc_requests


def get_node_tip_hashes_list(conn=None):
    """
    Retrieves the current block dag info details and parses the "tipHashes".

    :return: The "tipHashes" result as a list
    """
    response = json_rpc_requests.get_block_dag_info_request(conn)
    tip_hash_list = response["result"]["tipHashes"]
    return tip_hash_list


def get_node_bits(url=None):
    """
    Retrieves the bits info details from get_block_template_request()

    :return: The "bits" result as a string
    """
    response = json_rpc_requests.get_block_template_request(url)
    bits = response["result"]["bits"]
    return bits


def get_node_utxo_commitment(url=None):
    """
    Retrieves the current block dag utxo commitment from get_block_template_request()

    :return: utxo commitment as a string
    """
    response = json_rpc_requests.get_block_template_request(url)
    utxo_commitment = response["result"]["utxoCommitment"]
    return utxo_commitment


def get_node_id_merkle_root(url=None):
    """
    Retrieves the current block dag accepted id merkle root from get_block_template_request()

    :return: id merkle root as a string
    """
    response = json_rpc_requests.get_block_template_request(url)
    id_merkle_root = response["result"]["acceptedIdMerkleRoot"]
    return id_merkle_root


def get_coinbase_tx_data(url=None):
    """
    Retrieves the current block dag coinbase tx data from get_block_template_request()

    :return: coinbase_tx_data as a string
    """
    response = json_rpc_requests.get_block_template_request(url)
    tx_data = response["result"]["coinbaseTxn"]["data"]
    return tx_data


def get_block_data_status(block_hash, url=None):
    """
    Retrieves the status of a specific block data from get_block_request()

    :param block_hash: Hash of the requested block
    :return: action_status as a string
    """
    response = json_rpc_requests.get_block_request(block_hash, url)
    action_status = kaspy_tools.kaspad.kaspad_block_utils.error_handler(response["error"])
    return action_status


def get_block_data_parent_hash(block_hash, url=None):
    """
    Retrieves the parent hashes list of a specific block from get_block_request()

    :param block_hash: Hash of the requested block
    :return: The requested block parent hashes list
    """
    response = json_rpc_requests.get_block_request(block_hash, url)
    parent_hashes = response["result"]["parentHashes"]
    return parent_hashes


def get_block_full_data(block_hash, url=None):
    """
    Retrieves a specific block full range of data from get_block_request()

    :param block_hash: Hash of the requested block
    :return: The full data of the block
    """
    response = json_rpc_requests.get_block_request(block_hash, url)
    return response["result"]


def get_block_dag_num_of_blocks(url=None):
    """
    Retrieves the amount of blocks currently in the Block-DAG.

    :return: num_of_blocks as INT
    """
    response = json_rpc_requests.get_block_dag_info_request(url)
    num_of_blocks = response["result"]["blocks"]
    return num_of_blocks
