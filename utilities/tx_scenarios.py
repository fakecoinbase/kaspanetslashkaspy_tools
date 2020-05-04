"""
Some 'higher level' transaction scenarios.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.json_rpc import json_rpc_constants
from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.kaspad.utilities.dnld_blocks_and_utxo_set_command import download_blocks_and_utxc_set
from kaspy_tools.kaspad.utilities.make_transactions_command import make_new_transactions
from kaspy_tools.kaspa_model.kaspa_address import make_addresses
from kaspy_tools.local_run import run_dev

KT_logger = config_logger.get_kaspy_tools_logger()

def generate_transactions_from_genesis(*, addr_count=100, tx_count=100, block_count=3, conn=None ):

    """
    Parameters
    ----------
    key_count   The number of key pairs to create
    tx_count    the number of requested transactions

    Returns     a list with kaspa_model transaction objects
    -------
    """
    mining_address = run_dev.get_mining_address()
    addresses = make_addresses(addr_count)
    addresses[mining_address.get_address(prefix='kaspadev')] = mining_address
    # download three block - the genesis block + 2 more blocks
    utxo_list, v_blocks, r_blocks = download_blocks_and_utxc_set(block_count, conn=conn)

    tx_list = make_new_transactions(tx_count, utxo_list, addresses)
    return tx_list, v_blocks
