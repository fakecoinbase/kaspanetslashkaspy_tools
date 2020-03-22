"""
Some 'higher level' transaction scenarios.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.kaspad.utilities.dnld_blocks_and_utxo_set_command import download_blocks_and_utxc_set
from kaspy_tools.kaspad.utilities.make_transactions_command import make_new_transactions

local_logger = config_logger.get_local_logger('kaspy_tools')

def generate_transactions_from_genesis(*, key_count=100, tx_count=100, mining_address ):
    """

    Parameters
    ----------
    key_count   The number of key pairs to create
    tx_count    the number of requested transactions

    Returns     a list with kaspa_model transaction objects
    -------

    """
    addresses = [KaspaAddress() for i in range(key_count)]
    addresses.append(mining_address)
    # download a single block - the genesis block
    utxo_set, v_blocks, r_blocks = download_blocks_and_utxc_set('http://127.0.0.1:16610/', 1)
    tx_list = make_new_transactions(tx_count, utxo_set, keys)
    return tx_list


