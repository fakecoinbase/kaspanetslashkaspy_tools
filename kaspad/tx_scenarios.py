"""
Some 'higher level' transaction scenarios.
"""
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.kaspa_dags.dnld_utxo_set_command import download_utxo_set
from kaspy_tools.kaspad.utilities.make_transactions_command import make_new_transactions
from kaspy_tools.kaspa_model.kaspa_address import make_addresses
from kaspy_tools.kaspad.utilities.coinbase_info import CoinbaseInfo
from kaspy_tools.kaspad.kaspa_dags.dag_tools import find_in_dag

KT_logger = config_logger.get_kaspy_tools_logger()

def generate_transactions_from_dag(*, addr_count=100, tx_count=100, block_count=None, miner_address, conn=None):
    """
    Generate transaction based on a DAG already submitted.
    :param addr_count: How many new parivate addresses to create
    :param tx_count: How many transactions to create
    :param block_count: How many blocks to use as a basis for the creation
    :param conn: A connection to the kaspad
    :return: A tupple: (list of TXs, all vblocks used, list of addresses used)
    """
    addresses = make_addresses(addr_count)          # make new addresses (dictionary)
    addresses[miner_address.get_address()] = miner_address

    # download all blocks
    utxo_list, v_blocks, r_blocks = download_utxo_set(block_count, conn=conn)

    tx_list = make_new_transactions(count=tx_count, utxo_list=utxo_list, addresses=addresses)
    return tx_list, v_blocks, addresses

def generate_double_spend_tx_pair(*, conn=None, miner_address):
    addresses = make_addresses(5)
    addresses[miner_address.get_address()] = miner_address
    # download all blocks
    utxo_list, v_blocks, r_blocks = download_utxo_set(block_count=300, conn=conn)
    utxo_list_a = utxo_list[1:3]                    # [0,1]
    utxo_list_b = [utxo_list[1], utxo_list[3]]    # [0,2]

    tx_list1 = make_new_transactions(count=1, utxo_list=utxo_list_a, addresses = addresses, in_count=2)
    for utxo in utxo_list_a:
        utxo['used'] = False
    tx_list2 = make_new_transactions(count=1, utxo_list=utxo_list_b, addresses = addresses, in_count=2)
    return tx_list1+tx_list2, v_blocks


def validate_coinbase_of_three(conn=None):
    block = find_in_dag.find_block_with_at_least_parents(min_parents=3, conn=conn)
    cb_info = CoinbaseInfo(paying_block_hash_bytes=bytes.fromhex(block['hash']),
                           coinbase_tx_bytes=bytes.fromhex(block['rawRx'][0]['hex']), conn=conn)
    paid_blocks_dict = cb_info.paid_blocks
    for hash, paid_block in paid_blocks_dict.items():
        print(len(paid_block.accepted_transactions))

    pass
