"""
Some 'higher level' transaction scenarios.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.kaspa_dags.dnld_utxo_set_command import download_utxo_set
from kaspy_tools.kaspad.utilities.make_transactions_command import make_new_transactions
from kaspy_tools.kaspa_model.kaspa_address import make_addresses
from kaspy_tools.local_run import run_dev

KT_logger = config_logger.get_kaspy_tools_logger()

def generate_transactions_from_dag(*, addr_count=100, tx_count=100, block_count=None, conn=None):
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
    # download all blocks
    utxo_list, v_blocks, r_blocks = download_utxo_set(block_count, conn=conn)

    tx_list = make_new_transactions(count=tx_count, utxo_list=utxo_list, addresses=addresses)
    return tx_list, v_blocks

def generate_double_spend_tx_pair(*, conn=None):
    mining_address = run_dev.get_mining_address()
    addresses = make_addresses(5)
    addresses[mining_address.get_address(prefix='kaspadev')] = mining_address
    # download all blocks
    utxo_list, v_blocks, r_blocks = download_utxo_set(block_count=10, conn=conn)
    utxo_list_a = utxo_list[1:3]                    # [0,1]
    utxo_list_b = [utxo_list[1], utxo_list[3]]    # [0,2]

    tx_list1 = make_new_transactions(count=1, utxo_list=utxo_list_a, addresses = addresses, in_count=2)
    for utxo in utxo_list_a:
        utxo['used'] = False
    tx_list2 = make_new_transactions(count=1, utxo_list=utxo_list_b, addresses = addresses, in_count=2)
    return tx_list1+tx_list2, v_blocks
