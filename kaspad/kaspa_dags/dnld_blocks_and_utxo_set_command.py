"""
This module can be used to compute the utxo set.
It does so by downloading blocks from a kaspad using json-rpc.
It then uses the downloaded blocks, and computes the utxo set that matches those blocks.
Call download_blocks_and_utxo_set to get the utxo set and the blocks.
"""
import json
from _datetime import datetime

from kaspy_tools.kaspad import kaspad_block_utils
from kaspy_tools.kaspad import json_rpc_client
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.kaspa_model import tx_out
from kaspy_tools.kaspa_model import tx_script
import kaspy_tools.kaspa_model.tx


def download_blocks_and_utxo_set(block_count, save_location=None, conn=None):

    raw_blocks, verbose_blocks = kaspad_block_utils.get_blocks(block_count, conn=conn)

    # utxo_list = compute_utxo_list(verbose_blocks)
    utxo_list = collect_utxo(verbose_blocks=verbose_blocks, conn=conn)
    if save_location is not None:
        save_raw_blocks(raw_blocks, save_location)
        save_utxo_set(utxo_list, save_location)
    return utxo_list, verbose_blocks, raw_blocks


def make_file_name(save_location, file_type, data_len):
    """
    Create a file name for a utxo set file, and a raw blocks file
    Parameters
    ----------
    save_location    a target directory for the file
    file_type        (str) 'raw-blocks-'   or      'utxc-set-'
    data_len         Number of records

    Returns          (str) the requested file name
    -------

    """
    timestamp = str(datetime.now()).replace(' ', '-')[:-7]
    timestamp = timestamp.replace(':', '-')
    ret_val = save_location + file_type + data_len + '-' + timestamp
    return ret_val


def save_raw_blocks(raw_blocks, save_location):
    """
    Save raw blocks to a file.
    Parameters
    ----------
    raw_blocks      an iterable of blocks
    save_location   target directory for file

    Returns         None
    -------

    """
    filename = make_file_name(save_location, 'raw-blocks-', str(len(raw_blocks)))

    with open(filename, 'w') as raw_blocks_file:
        for block in raw_blocks:
            print(block, file=raw_blocks_file)


def save_utxo_set(utxc_set, save_location):
    """
    Save utxo set to a file.
    Parameters
    ----------
    utxo_set        an iterable of utxos'
    save_location   target directory for file

    Returns         None
    -------

    """
    filename = make_file_name(save_location, 'utxc-set-', str(len(utxc_set)))

    with open(filename, 'w') as utxc_set_file:
        for (tx_id, out_idx), tx_out in utxc_set.items():
            print(json.dumps([tx_id, out_idx, tx_out.get_value(), tx_out.get_script_pub_key()]), file=utxc_set_file)


def compute_utxo_list(all_verbose_blocks):
    """
    This function works by iterating over all transactions, and extracting all utxo into a
    utxo list.
    Each time an input references an output(utxo), the function removes this utxo from the list.
    It then populate the utxo dictionary with new outputs.
    :param all_verbose_blocks: A list containing all verbose blocks
    :return: The utxo_list
    """

    utxo_list = [] # keep a list to have them ordered
    for block in all_verbose_blocks:
        for tx in block['rawRx']:
            if tx['subnetwork'] == kaspy_tools.kaspa_model.tx.COINBASE_SUBNETWORK:  # so this is a coinbase transaction
                collect_coinbase_utxo(tx, utxo_list)
            else:
                collect_tx_utxo(tx, utxo_list)

    return utxo_list

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

    utxo_list = utxo_from_ordered_tx_list(tx_ordered_list)
    return utxo_list

def utxo_from_ordered_tx_list(tx_ordered_list):
    utxo_list = []
    for tx in tx_ordered_list:
        if tx['subnetwork'] == kaspy_tools.kaspa_model.tx.COINBASE_SUBNETWORK:  # so this is a coinbase transaction
            collect_coinbase_utxo(tx, utxo_list)
        else:
            collect_tx_utxo(tx, utxo_list)

    return utxo_list

def collect_tx_utxo(tx, utxo_list):
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
        if referred_out in utxo_list:
            del (utxo_list[referred_out])
            utxo_list.remove()

    # ..then add outputs from transaction into utxo_set
    for index, vout in enumerate(tx['vout']):
        utxo_list[(tx['txId'], index)] = tx_out.TxOut(vout['value'], 0, vout['scriptPubKey'])

    return utxo_list


def collect_coinbase_utxo(tx, utxo_list):
    """
    This function gets a json encoded coinbase transaction from a block.
    It convert these vin inputs into a utxo dictionary (encoded the same as in get_utxo_set)
    :param utxo_set: The set of utxo collected
    :param tx: a json encoded transaction
    :return: utxo_set created from coinbase vin inputs
    """
    for index, vout in enumerate(tx['vout']):
        # scriptPubKey = tx_script.TxScript.script_sig_factory(sig='', public_key=vout['scriptPubKey']['hex'][6:46])
        scriptPubKey = tx_script.TxScript.parse_tx_script(raw_script=vout['scriptPubKey']['hex'])
        new_utxo = {
            'output':tx_out.TxOut.tx_out_factory(value=vout['value'], script_pub_key=scriptPubKey,
                                                 tx_id=tx['txId'], out_index=index),
            'used':False
        }
        utxo_list.append(new_utxo)

    return utxo_list
