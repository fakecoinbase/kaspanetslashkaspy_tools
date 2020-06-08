"""
This file holds all the constant elements that are being used by the kaspa-d automation.
"""
import os
from kaspy_tools.kaspy_tools_constants import KASPAD_TOP_PATH

# Path for the local KASPAD folder

# Path for the binary file of a valid empty block
VALID_BLOCK_EMPTY_PATH = KASPAD_TOP_PATH + "/blocks_cartridge/valid_block_empty.dat"

# Path for the binary file of valid 1848 block
VALID_1848_BLOCKS_PATH = KASPAD_TOP_PATH + "/blocks_cartridge/1848_blocks.dat"

# Path for the binary file of valid 2138 block
VALID_2138_BLOCKS_PATH = KASPAD_TOP_PATH + "/blocks_cartridge/2138_blocks.dat"

# The max value possible of uint64
MAX_UINT64 = 0xffffffffffffffff

# Hash of Genesis block (devnet)
GENESIS_HASH = "000033abb09b45e09ef5e3a2b92185b7503a074565ef5706904167c60b37d6f4"
# GENESIS_HASH = "f4d6370bc66741900657ef6545073a50b78521b9a2e3f59ee0459bb0ab330000"

# Finality value (devnet)
FINALITY_DEVNET = 1000

# Phantom K
PHANTOM_K = 10

# Block has string (hex) slice, to be used in logs, drawing etc.
PARTIAL_HASH_SIZE = -10
