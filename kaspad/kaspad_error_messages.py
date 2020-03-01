"""
This module holds a list of error messages that can be received from the node and used during the run of the test kits.
"""

# Finality error message
finality_error_message = "Error Code: -25, Error Message: Block rejected. Reason: block 000033abb09b45e09ef5e3a2b92185b7503a074565ef5706904167c60b37d6f4 is a finalized parent "

# Incorrect signature script error message
incorrect_signature_script_error_message = "Error Code: -22, Error Message: Block decode failed: readScript: transaction input " \
                                "signature script is larger than the max allowed size "

# Orphan block error message
orphan_block_error_message = "Error Code: -6, Error Message: Block is an orphan"

# unexpected EOF error message
unexpected_EOF_error_message = "Error Code: -22, Error Message: Block decode failed: unexpected EOF"

# block rejected due to _timestamp smaller then 0 error message
incorrect_timestamp_error_message = "Error Code: -25, Error Message: Block rejected. Reason: block _timestamp of " \
                                    "1969-12-31 23:59:59 +0000 UTC is not after expected 2019-10-16 10:47:40 +0000 UTC"

# block rejected due to wrong difficulty (high)
too_high_difficulty_error_message = "Error Code: -25, Error Message: Block rejected. Reason: block target difficulty of" \
                                 " 31e7f0000000000000000000000000000000000000000000000000000000000000000000000000000000" \
                                 "0000000000000000000000000000000000000000000000000000000000000000000000000000000" \
                                 " is higher than max of 00007fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

# block rejected due to wrong difficulty (low)
too_low_difficulty_error_message = "Error Code: -25, Error Message: Block rejected. Reason: block target difficulty of " \
                                   "0000000000000000000000000000000000000000000000000000000000000000 is too low"

# block rejected due to hash higher than expected
hash_higher_than_expected_error_message = "Error Code: -25, Error Message: Block rejected. Reason: block hash of " \
                                          "f985b34149aa729dc8e7a7cdd9ff9373f99ad2e7664af03bb94e301ce24c4d9c is higher " \
                                          "than expected max of 00007fffff000000000000000000000000000000000000000000000000000000"

