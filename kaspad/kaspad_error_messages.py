"""
This module holds a list of error messages that can be received from the node and used during the run of the test kits.
"""

# block rejected due to hash higher than expected
HASH_HIGHER_THAN_EXPECTED_ERROR_MESSAGE = 'Block rejected. Reason: block hash  higher than expected max '

# block rejected due to already been mined
BLOCK_ALREADY_MINED_ERROR_MESSAGE = 'Block rejected. Reason: already have  block'

# block rejected due to already been in the orphan pool
BLOCK_ALREADY_IN_ORPHAN_POOL_ERROR_MESSAGE = 'Block rejected. Reason: already have block (orphan)'

# block rejected due to timestamp older than expected
BLOCK_TIMESTAMP_TOO_OLD_ERROR_MESSAGE = 'Block rejected. Reason: block timestamp of 1970-01-01 02:13:34.17 +0000 UTC ' \
                                        'is not after expected'

# block rejected due to version mismatching expected
BLOCK_VERSION_TOO_LOW_OR_TOO_HIGH_ERROR_MESSAGE = 'Block decode failed: unexpected EOF'

# block not found
BLOCK_NOT_FOUND_ERROR_MESSAGE = 'Block not found'

# Orphan block error message
orphan_block_error_message = "Error Code: -6, Error Message: Block is an orphan"