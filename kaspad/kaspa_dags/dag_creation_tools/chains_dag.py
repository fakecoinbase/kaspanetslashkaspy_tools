import os
import subprocess
from kaspy_tools.local_run.run_local_services import run_services
from kaspy_tools.kaspad import kaspad_constants
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.kaspad.utilities import block_generator
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.logs import config_logger

KT_logger = config_logger.get_kaspy_tools_logger()

def make_and_submit_single_chain(*, floors=None, pay_address, conn):
    if not floors:
        floors=[]
    for f in floors:
        floor_blocks = []
        for b in range(f):
            new_block, block_hash = block_generator.generate_valid_block_from_template(conn=conn, native_txs=[],
                                                                                       pay_address=pay_address)
            floor_blocks.append(new_block)
        for block in floor_blocks:
            response, response_json = json_rpc_requests.submit_block_request(block.hex(), options=None, conn=conn)

def get_current_blocks(conn):
    raw_blocks, verbose_blocks = json_rpc_requests.get_blocks(requested_blocks_count=200, conn=conn)
    return raw_blocks

def submit_saved_blocks(saved_blocks, conn):
    for block in saved_blocks:
        response, response_json = json_rpc_requests.submit_block_request(block, options=None, conn=conn)

def clean_blocks():
    run_services.remove_all_localrun_containers()
    run_services.clear_kaspad_volume_files()

def get_blocks_from_chain(*, chain_definition=None, clear=True, pay_address, conn):
    if clear:
        clean_blocks()
        run_services.run_kaspanet_services()
    make_and_submit_single_chain(floors=chain_definition, pay_address=pay_address, conn=conn)
    chain_blocks = get_current_blocks(conn=conn)
    return chain_blocks


def make_chains_dag(conn, pay_address):
    chain_one = get_blocks_from_chain(chain_definition=[1,1,1,1,1], conn=conn, pay_address=pay_address)
    # when we get the blocks for chain_two, we clean blocks of chain_one
    chain_two = get_blocks_from_chain(chain_definition=[2,1], conn=conn, pay_address=pay_address)
    # Now chain_two is submitted, we submit chain_one
    submit_saved_blocks(saved_blocks=chain_one, conn=conn)
    # Now chain_one AND chain_two are submitted
    # getting chain_three without clearing:
    chain_three = get_blocks_from_chain(chain_definition=[1 for i in range(110)], clear=False, conn=conn,
                                        pay_address=pay_address)
    # now submit


