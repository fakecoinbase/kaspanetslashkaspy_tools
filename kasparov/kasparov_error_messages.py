
# General Server Error
server_error_code = 500
server_error_message = "a server error occurred"

# /Blocks Error
blocks_limits_error_code = 400
blocks_limits_error_message = "limit higher than 100 or lower than 1 was requested"

blocks_empty_parameters_error_code = 422
blocks_empty_order_error_message = "'' is not a valid order"
blocks_empty_skip_error_message = "Couldn't parse the 'skip' query parameter"
blocks_empty_limit_error_message = "Couldn't parse the 'limit' query parameter"

blocks_skip_minus_one_error_code = 400
blocks_skip_minus_one_error_message = "skip lower than 0 was requested"

# /block/{hash} Errors
block_was_not_found_error_code = 404
block_was_not_found_error_message = "no block with the given block hash was found"

block_hash_not_hex_encoded_error_code = 422
block_hash_not_hex_encoded_error_message = "the given block hash is not a hex-encoded 32-byte hash"

# /utxos/{address} Error
utxos_address_not_well_formatted_error_code = 422
utxos_address_not_well_formatted_error_message = "The given address is not a well-formatted P2PKH or P2SH address"

# /transactions/address/{address} Errors
transactions_limits_error_code = 400
transactions_limits_error_message = "limit higher than 1000 or lower than 1 was requested"

transactions_address_not_well_formatted_error_code = 422
transactions_address_not_well_formatted_error_message = "The given address is not a well-formatted " \
                                                        "P2PKH or P2SH address"

transactions_empty_parameters_error_code = 422
transactions_empty_skip_error_message = "Couldn't parse the 'skip' query parameter"
transactions_empty_limit_error_message = "Couldn't parse the 'limit' query parameter"

transactions_skip_minus_one_error_code = 400
transactions_skip_minus_one_error_message = "skip lower than 0 was requested"


# /fee-estimates Error
# Only uses the server error code 500

# /transaction/id/{txid} Errors
transaction_id_not_found_error_code = 404
transaction_id_not_found_error_message = "no transaction with the given txid was found"

transaction_id_not_hex_encoded_error_code = 422
transaction_id_not_hex_encoded_error_message = "The given txid is not a hex-encoded 32-byte hash"

# /transaction/hash/{txhash} Errors
transaction_hash_not_found_error_code = 404
transaction_hash_not_found_error_message = "no transaction with the given txhash was found"

transaction_hash_not_hex_encoded_error_code = 422
transaction_hash_not_hex_encoded_error_message = "The given txhash is not a hex-encoded 32-byte hash"

# POST /transaction Errors
transaction_not_well_formatted_error_code = 422
transaction_not_well_formatted_error_message = "the raw transaction is not a hex-encoded transaction"

transaction_rejected_error_code = 422
transaction_rejected_error_message = "-25: TX rejected"
