"""
Some 'higher level' transaction scenarios.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.utilities import make_keys_command
from kaspy_tools.utilities.dnld_blocks_and_utxo_set_command import download_blocks_and_utxc_set
from kaspy_tools.utilities.make_transactions_command import make_new_transactions

local_logger = config_logger.get_local_logger(__name__)

def generate_transactions_from_genesis(*, key_count=100, tx_count=100 ):
    """

    Parameters
    ----------
    key_count   The number of key pairs to create
    tx_count    the number of requested transactions

    Returns     a list with kaspa_model transaction objects
    -------

    """
    local_logger.info('Generating commands from genesis.')
    keys = make_keys_command.create_public_and_private_keys(key_count)

    # download a single block - the genesis block
    utxo_set, v_blocks, r_blocks = download_blocks_and_utxc_set('http://127.0.0.1:16610/', 1)
    tx_list = make_new_transactions(tx_count, utxo_set, keys)
    return tx_list


