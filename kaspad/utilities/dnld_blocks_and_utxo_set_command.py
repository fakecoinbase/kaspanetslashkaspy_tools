"""
This module can be used to compute the utxo set.
It does so by downloading blocks from a kaspad using json-rpc.
It then uses the downloaded blocks, and computes the utxo set that matches those blocks.
Call download_blocks_and_utxc_set to get the utxo set and the blocks.
"""
import json
from _datetime import datetime

import kaspy_tools.kaspad.kaspad_utils
from kaspy_tools.kaspad import json_rpc_client
from kaspy_tools.model import tx_out
from kosmos.k_agent.logs import config_logger

local_logger = config_logger.get_local_logger(__name__)


def download_blocks_and_utxc_set(url, block_count, save_location=None):
    """
    First downloads blocks, then computes the utxo set.
    It saves the blocks to a file if requested.
    Parameters
    ----------
    url             pointing to the kaspad (url should include port number)
    block_count     how many blocks to download
    save_location   if given, a directory in which to save raw blocks and utxo

    Returns         3 item tuple with utxo-set,  verbose_blocks, raw_blocks
    -------

    """
    raw_blocks, verbose_blocks = kaspy_tools.kaspad.kaspad_utils.get_blocks(url, block_count)
    utxo_set = compute_utxo_set(verbose_blocks)
    if save_location is not None:
        save_raw_blocks(raw_blocks, save_location)
        save_utxo_set(utxo_set, save_location)
    return utxo_set, verbose_blocks, raw_blocks


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


def compute_utxo_set(all_verbose_blocks):
    """
    This function works by iterating over all transactions, and extracting all utxo into a
    utxo dictionary (utxo_set).
    Each time an input references an output(utxo), the function removes this utxo from the list.
    It then populate the utxo dictionary with new outputs.
    The utxo_set keys are tuples of the form:  (transaction_hash, output_index)
    The values are tx_out objects.
        :param all_verbose_blocks: A list containing all verbose blocks
    :return: The utxo_set dictionary
    """

    utxo_set = {}
    for block in all_verbose_blocks:
        for tx in block['rawRx']:
            if tx['subnetwork'] == tx.COINBASE_SUBNETWORK:  # so this is a coinbase transaction
                utxo_set.update(collect_coinbase_utxo(tx, utxo_set))
            else:
                utxo_set.update(collect_tx_utxo(tx, utxo_set))

    return utxo_set


def collect_tx_utxo(tx, utxo_set):
    """
    Go over the inputs and outputs of a non coinbase transaction.
    Use inputs to delete matching utxo
    :param tx: current transaction
    :param utxo_set: The set of utxo collected
    :return:
    """
    # first, go over input, and remove matching utxo outputs
    for index, vin in enumerate(tx['vin']):
        referred_out = (vin['txId'], vin['vout'])
        if referred_out in utxo_set:
            del (utxo_set[referred_out])

    # ..then add outputs from transaction into utxo_set
    for index, vout in enumerate(tx['vout']):
        utxo_set[(tx['txId'], index)] = tx_out.TxOut(vout['value'], 0, vout['scriptPubKey'])

    return utxo_set


def collect_coinbase_utxo(tx, utxo_set):
    """
    This function gets a json encoded coinbase transaction from a block.
    It convert these vin inputs into a utxo dictionary (encoded the same as in get_utxo_set)
    :param utxo_set: The set of utxo collected
    :param tx: a json encoded transaction
    :return: utxo_set created from coinbase vin inputs
    """
    for index, vout in enumerate(tx['vout']):
        utxo_set[(tx['txId'], index)] = tx_out.TxOut(vout['value'], 0, vout['scriptPubKey'])

    return utxo_set
