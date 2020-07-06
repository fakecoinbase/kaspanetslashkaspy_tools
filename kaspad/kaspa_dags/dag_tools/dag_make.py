import random
from kaspy_tools.kaspad import kaspad_constants
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.utilities import block_generator
from kaspy_tools.kaspad.json_rpc import json_rpc_requests

KT_logger = config_logger.get_kaspy_tools_logger()


def make_dag(floors=10, min_width=3, max_width=6, conn=None):
    for f in range(floors):
        floor_list = make_floor(min_width=min_width, max_width=max_width, conn=conn)
        submit_floor(floor_list=floor_list, conn=conn)
        KT_logger.debug('Floor # %d created.', f)

def make_floor(*, min_width, max_width, conn):
    floor_list=[]
    num_elements = random.randint(min_width,max_width)
    KT_logger.debug('Number of blocks in floor: %d.', num_elements)
    for b in range(num_elements):
        new_block, block_hash = block_generator.generate_valid_block_from_template(conn=conn, native_txs=[],
                                                                                   netprefix='kaspasim')
        KT_logger.debug('Created block hash: %s', block_hash.hex()[kaspad_constants.PARTIAL_HASH_SIZE:])
        floor_list.append(new_block)
    return floor_list

def submit_floor(*, floor_list=None, conn=None):
    if floor_list==None:
        floor_list=[]
    for block in floor_list:
        response, response_json = json_rpc_requests.submit_block_request(block.hex(),options=None,conn=conn)
        if response_json['result'] is not None:
            raise ValueError




def try_make_dag():
    make_dag()

if __name__ == '__main__':
    try_make_dag()