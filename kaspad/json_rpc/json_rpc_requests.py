"""
This module holds the methods that handle all the JSON-RPC requests for the automation project.
"""

import requests
import json
from kaspy_tools.kaspad.json_rpc import json_rpc_constants


def submit_block_request(hex_block, options=None, conn=None):
    """
    submitting a pre-defined block in hex string formant to the node via JSON-RPC.

    :param hex_block: Block in hexadecimal string
    :param options: dictionary with key workID {"workId": "value"}
    :return: returns the original response as well as reponse_json
        response_json holds 2 dictionaries and 1 variable:
        * result- {}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    if options is None:
        payload = {
            "method": "submitBlock",
            "params": [hex_block],
            "jsonrpc": "2.0",
            "id": 0,
        }
    else:
        payload = {
            "method": "submitBlock",
            "params": [hex_block, {"workId": "Jimmy"}],
            "jsonrpc": "2.0",
            "id": 0,
        }
    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response, response_json


def get_block_request(block_hash, sub_network=None, conn=None):
    """
    retrieving specific block data based on it's hash.

    :param block_hash: Hash of the block in string format
    :param sub_network: Name of a relevant sub-network. Must remain as "None" if no sub-network is relevant!
    :return: returns a response with 2 dictionaries and 1 variable:
        * result- {hash: "string", confirmations: int, size: int, height: int, _version: int, versionHex: string,
                hashMerkleRoot: "string", acceptedIdMerkleRoot: "string", tx: ["string"], time: int, _nonce: int,
                _bits: "string", difficulty: float, parentHashes: ["string"]}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    if sub_network is None:
        payload = {
            "method": "getBlock",
            "params": [block_hash, True, False],
            "jsonrpc": "2.0",
            "id": 0
        }
    else:
        payload = {
            "method": "getBlock",
            "params": [block_hash, True, False, sub_network],
            "jsonrpc": "2.0",
            "id": 0
        }
    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response_json


def get_best_block_request(conn=None):
    """
    retrieves the hash and the height of the selected TIP.

    :return: returns a response with 2 dictionaries and 1 variable:
        * result- {hash:"string", height: int}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getBestBlock",
        "params": [],
        "jsonrpc": "2.0",
        "id": 0,
    }
    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response_json


def get_block_dag_info_request(conn=None):
    """
    retrieves DAG information.

    :return: returns a response with 2 dictionaries and 1 variable:
        * result- {dag:"string", blocks: int, headers: int, tipHashes: ["string"], difficulty: float, medianTime: int
                utxoCommitment: "string", pruned: Boolean, softForks: ???, bip9SoftForks: [nested list]}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getBlockDagInfo",
        "params": [],
        "jsonrpc": "2.0",
        "id": 0,
    }
    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response_json


def generate_request(num_blocks, conn=None):
    """
    Generates an X amount of blocks based on received parameter.

    :param num_blocks: The amount of blocks to be generated
    :return: String "Done"
    """
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "generate",
        "params": [num_blocks],
        "jsonrpc": "2.0",
        "id": 0,
    }
    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response_json


def get_block_template_request(conn=None):
    """
    Retrieves up to date block template.

    :return: returns a response with 2 dictionaries and 1 variable:
        * result- {_bits: "string", curTime: int, height: int, parentHashes: [list of stings], massLimit: int,
                transactions: [list of strings], acceptedIdMerkleRoot: "string", 'utxoCommitment': "string",
                _version: int, coinbaseTxn: {data: "string", id: "string", depends: [list], mass: int, fee: int},
                longPollId: "string", target: "string", maxTime: int, minTime: int,
                mutable: [time, transactions/add, parentblock, coinbase/append], nonceRange: "string",
                capabilities: [proposal]},}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getBlockTemplate",
        "params": [{"capabilities": ["coinbasetxn", "workid", "coinbase/append"]}],
        "jsonrpc": "2.0",
        "id": 0,
    }
    payload_json = json.dumps(payload)

    response = requests.get(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response_json


def get_blocks(requested_blocks_count, conn=None):
    """
    This function returns a list of blocks, in binary-hex encoding and verbose encoding.
    The blocks are taken from a node specified in node_url.
        :param node_url: The url of a kaspad node.
        :param requested_blocks_count specify the number of requested blocks
    :return: (raw blocks list, verbose blocks list)   None in each part if not requested.
    """

    all_raw_blocks = []
    all_verbose_blocks = []
    blocks_count = 0
    headers = {'content-type': 'application/json'}
    next_hash = None
    # Params in the next jsonrpc means:  False - do not include binary representation , True-include verbose data
    payload = {"method": "getBlocks", "params": [True, True, None],  # Always get raw AND verbose
               "jsonrpc": "2.0",
               "id": 0}

    while True:
        if next_hash is not None:
            payload['params'][2] = next_hash
        payload_json = json.dumps(payload)

        response = requests.get(conn.updated_url, data=payload_json, headers=headers, auth=('user', 'pass'),
                                verify=conn.cert_file_path)
        response_json = response.json()
        all_verbose_blocks.extend(response_json['result']['verboseBlocks'])
        all_raw_blocks.extend(response_json['result']['rawBlocks'])
        next_hash = all_verbose_blocks[-1]['hash']

        blocks_count += len(response_json['result']['verboseBlocks'])
        if blocks_count >= requested_blocks_count:
            all_verbose_blocks = all_verbose_blocks[:requested_blocks_count]
            all_raw_blocks = all_raw_blocks[:requested_blocks_count]
            break
    return all_raw_blocks, all_verbose_blocks


def submit_raw_tx(tx_hex, options=None, conn=None):
    """
    submitting a pre-defined tx in hex string formant to the node via JSON-RPC.

    :param tx_hex: tx in hexadecimal string
    :param options: dictionary with key workID {"workId": "value"}
    :return: returns the original response as well as reponse_json
        response_json holds 2 dictionaries and 1 variable:
        * result- {}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    if options is None:
        payload = {
            "method": "sendRawTransaction",
            "params": [tx_hex],
            "jsonrpc": "2.0",
            "id": 0,
        }
    else:
        payload = {
            "method": "sendRawTransaction",
            "params": [tx_hex, {"workId": "Jimmy"}],
            "jsonrpc": "2.0",
            "id": 0,
        }
    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response, response_json


def get_mempool_entry_request(tx_id, conn=None):
    """
    retrieving specific mempool entery (raw_tx) data based on tx_id.

    :param tx_id: tx_id of the tx in string format
    :return: returns a response with 2 dictionaries and 1 variable:
        * result- {hash: "string", confirmations: int, size: int, height: int, _version: int, versionHex: string,
                hashMerkleRoot: "string", acceptedIdMerkleRoot: "string", tx: ["string"], time: int, _nonce: int,
                _bits: "string", difficulty: float, parentHashes: ["string"]}
        * error- {code: int, message: "string"}
        * id
    """
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getMempoolEntry",
        "params": [tx_id],
        "jsonrpc": "2.0",
        "id": 0
    }

    payload_json = json.dumps(payload)

    response = requests.post(conn.updated_url, data=payload_json, headers=headers,
                             verify=conn.cert_file_path)
    response_json = response.json()
    return response_json



def get_peer_info_request(conn=None):
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getPeerInfo",
        "params": [],
        "jsonrpc": "2.0",
        "id": 0
    }

    payload_json = json.dumps(payload)

    response = requests.get(conn.updated_url, data=payload_json, headers=headers,
                            verify=conn.cert_file_path)
    response_json = response.json()
    return response_json
    pass