import random
import queue
from kaspy_tools.kaspad import kaspad_constants
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspad.utilities import block_generator
from kaspy_tools.kaspad.json_rpc import json_rpc_requests

KT_logger = config_logger.get_kaspy_tools_logger()


def make_realistic_dag(batch_count=3, min_width=1, max_width=3, conn=None):
    block_queue = queue.Queue()
    for f in range(batch_count):
        batch = make_batch_into_queue(min_width=min_width, max_width=max_width, queue=block_queue, conn=conn)
        submit_some_blocks(queue=block_queue, min_width=min_width, max_width=max_width, conn=conn)
        KT_logger.debug('Floor # %d created.', f)

def make_batch_into_queue(*, min_width, max_width, queue=None, conn=None):
    num_elements = random.randint(min_width,max_width)
    KT_logger.debug('Number of blocks in batch: %d.', num_elements)
    for b in range(num_elements):
        new_block, block_hash = block_generator.generate_valid_block_from_template(conn=conn, native_txs=[])
        KT_logger.debug('Created block hash: %s', block_hash.hex()[kaspad_constants.PARTIAL_HASH_SIZE:])
        queue.put(new_block)

def submit_some_blocks(*, queue=None, min_width, max_width, conn=None):
    q_size = queue.qsize()
    KT_logger.debug('Queue size: %d.', q_size)
    rand_count = random.randint(q_size//2, q_size)
    for i in range(rand_count):
        block = queue.get()
        response, response_json = json_rpc_requests.submit_block_request(block.hex(),options=None,conn=conn)
