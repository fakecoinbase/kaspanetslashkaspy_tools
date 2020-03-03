import json
import datetime
from kosmos.k_agent.logs import config_logger

local_logger = config_logger.get_local_logger(__name__)


def load_raw_blocks_from_file(target_dir, raw_blocks_fname):
    """
    Load and return raw blocks from a file.
    Parameters
    ----------
    target_dir        A directory where block file is located
    raw_blocks_fname  Blocks file name

    Returns           None
    -------

    """
    raw_blocks_list = []
    raw_blocks_fname = target_dir + raw_blocks_fname
    with open(raw_blocks_fname, 'r') as raw_blocks_file:
        for block in raw_blocks_file:
            raw_blocks_list.append(block)
    return raw_blocks_list


def load_utxo_from_file(target_dir, utxo_list_fname):
    """
        Load and return raw blocks from a file.
        Parameters
        ----------
        target_dir        A directory where utxo set file is located
        utxo_list_fname   utxo set file name

        Returns           None
        -------
        """
    utxo_set = {}
    utxo_list_fname = target_dir + utxo_list_fname
    with open(utxo_list_fname, 'r') as utxc_set_file:
        for utxo in utxc_set_file:
            json_utxo = json.loads(utxo)
            # Enter the new utxo into the utxo dictionary.
            value = json_utxo[2]
            script = json_utxo[3]
            is_used = False
            utxo_set[(json_utxo[0], json_utxo[1])] = [value, script, is_used]
    return utxo_set


def save_utxo_set(utxc_set, target_dir, filename=''):
    """
    Saves a utxo set in a file
    Parameters
    ----------
    utxc_set    The utxo to save
    target_dir  A directory to use
    filename    The filename to creat

    Returns     None
    -------

    """
    if not filename:
        timestamp = str(datetime.now()).replace(' ', '-')[:-7]
        timestamp = timestamp.replace(':', '-')
        filename = target_dir + 'utxc-set-' + str(len(utxc_set)) + '-' + timestamp
    with open(filename, 'w') as utxc_set_file:
        for (tx_id, out_idx), tx_out in utxc_set.items():
            print(json.dumps([tx_id, out_idx, tx_out.get_value(), tx_out.get_script_pub_key()]), file=utxc_set_file)
