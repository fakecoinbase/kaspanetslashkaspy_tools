"""
This module holds the expected responses for the different CLI Wallet commands.
"""

# Create command response
create_command_response = [
    "This is your private key, granting access to all wallet funds. Keep it safe. Use it only when sending Kaspa.\n",
    "Private key (hex):\t", "\n", "These are your public addresses for each network, where money is to be sent.\n",
    "Address (mainnet):\t", "Address (testnet):\t", "Address (devnet):\t"]

# Balance command response
balance_command_positive_response = ["Balance:\t\tKAS"]


# Invalid public address error message
invalid_balance_command_public_address = [
    'Error reading UTXOs from Kasparov server response: Response status 422 Unprocessable Entity\n',
    'ResponseBody:\n',
    '{"errorCode":422,"errorMessage":"The given address is not a well-formatted P2PKH or P2SH address."}\n']

# Invalid Kasparov address error message
invalid_kasparov_address = ['Error getting UTXOs from Kasparov server', ' Get http',
                            '//kasparov/utxos/address/kaspadev', ' dial tcp', ' lookup kasparov', ' no such host\n']


# Send command response
send_command_positive_response = [
    "Transaction was sent successfully\n",
    "Transaction ID:"]

# Send command invalid public address error message
invalid_send_command_public_address = ['decoded address is of unknown format: invalid index of \':\'\n']

# Send command invalid private key error message
invalid_send_command_private_key = ['Error parsing private key hex: encoding/hex: odd length hex string\n']
