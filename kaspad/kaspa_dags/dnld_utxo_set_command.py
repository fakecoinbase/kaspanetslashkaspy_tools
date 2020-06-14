"""
This module computes the utxo set.
It does so by downloading blocks from a kaspad using json-rpc.
It then uses the downloaded blocks, and computes the utxo set that matches those blocks.
Call download_utxo_set to get the utxo set and the blocks.
"""
from kaspy_tools.kaspad import kaspad_block_utils
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.kaspa_model import tx_out
from kaspy_tools.kaspa_model import tx_script
import kaspy_tools.kaspa_model.tx


def download_utxo_set(block_count, save_location=None, conn=None):
    raw_blocks, verbose_blocks = kaspad_block_utils.get_blocks(block_count, conn=conn)
    utxo_list = collect_utxo(verbose_blocks=verbose_blocks, conn=conn)
    return utxo_list, verbose_blocks, raw_blocks


def collect_utxo(*, conn=None, verbose_blocks=None):
    tx_ordered_list = []
    result = json_rpc_requests.get_chain_from_block(start_hash=None, conn=conn, include_blocks=False)
    blocks_dict = {block['hash']: block for block in verbose_blocks}
    added_blocks = result['result']['addedChainBlocks']
    for block in added_blocks:
        for accepted_block in block['acceptedBlocks']:
            for tx in blocks_dict[accepted_block['hash']]['rawRx']:
                if tx['txId'] in accepted_block['acceptedTxIds']:
                    tx_ordered_list.append(tx)

    return utxo_from_ordered_tx_list(tx_ordered_list)


def utxo_from_ordered_tx_list(tx_ordered_list):
    utxo_list = []
    for tx in tx_ordered_list:
        if tx['subnetwork'] == kaspy_tools.kaspa_model.tx.COINBASE_SUBNETWORK:  # so this is a coinbase transaction
            collect_coinbase_tx_utxo(tx, utxo_list)
        else:
            collect_native_tx_utxo(tx, utxo_list)

    return utxo_list


def collect_native_tx_utxo(tx, utxo_dict):
    """
    Go over the inputs and outputs of a non coinbase transaction.
    Use inputs to delete matching utxo
    :param tx: current transaction
    :param utxo_set: The set of utxo collected
    :return:
    """
    # TODO: fix after changes
    # first, go over input, and remove matching utxo outputs
    for index, vin in enumerate(tx['vin']):
        referred_out = (vin['txId'], vin['vout'])
        if referred_out in utxo_dict:
            del (utxo_dict[referred_out])

    # ..then add outputs from transaction into utxo_set
    for index, vout in enumerate(tx['vout']):
        scriptPubKey = tx_script.TxScript.parse_tx_script(raw_script=vout['scriptPubKey']['hex'])
        new_utxo = {
            'output': tx_out.TxOut.tx_out_factory(value=vout['value'], script_pub_key=scriptPubKey,
                                                  tx_id=tx['txId'], out_index=index),
            'used': False
        }
        utxo_dict[(tx['txId'], index)] = new_utxo

    return utxo_dict


def collect_coinbase_tx_utxo(tx, utxo_list):
    """
    This function gets a json encoded coinbase transaction from a block.
    It convert these vin inputs into a utxo dictionary (encoded the same as in get_utxo_set)
    :param utxo_set: The set of utxo collected
    :param tx: a json encoded transaction
    :return: utxo_set created from coinbase vin inputs
    """
    for index, vout in enumerate(tx['vout']):
        scriptPubKey = tx_script.TxScript.parse_tx_script(raw_script=vout['scriptPubKey']['hex'])
        new_utxo = {
            'output': tx_out.TxOut.tx_out_factory(value=vout['value'], script_pub_key=scriptPubKey,
                                                  tx_id=tx['txId'], out_index=index),
            'used': False
        }
        utxo_list.append(new_utxo)

    return utxo_list
