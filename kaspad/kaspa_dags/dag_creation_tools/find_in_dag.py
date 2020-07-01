"""
DAG search utilities
"""
from kaspy_tools import kaspy_tools_constants

from kaspy_tools.kaspad import kaspad_block_utils

def find_block_with_at_least_parents(*, min_parents=1, v_blocks=None, conn=None):
    if v_blocks is None and conn is None:
        raise ValueError
    else:
        raw_blocks, verbose_blocks = kaspad_block_utils.get_blocks(kaspy_tools_constants.MAX_BLOCKS_IN_TESTS,
                                                                   conn=conn)
    for block in verbose_blocks:
        if len(block['parentHashes']) >= min_parents:
            return block
