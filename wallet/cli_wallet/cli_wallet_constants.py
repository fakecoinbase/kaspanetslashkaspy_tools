"""
This module holds the required constants for the CLI Wallet tests.
"""

from model import cli_wallet_user

# a pre-defined wallet that was created to be used in the CLI Wallet tests as the target for all the send tests
RECEIVER_ADDRESS = cli_wallet_user.CliWalletUser("7c81dc9ca68977f2b1dcdcc0f33eba66d80a247e6d453765b4d9c05ac000b4fd",
                                                 "kaspa:qr9my2690xehn4jm6yngeew0awq9vlsrdu4t2cqqxw",
                                                 "kaspatest:qr9my2690xehn4jm6yngeew0awq9vlsrdu92ecrmgv",
                                                 "kaspadev:qr9my2690xehn4jm6yngeew0awq9vlsrdu78xuxrtp")

CLI_WALLET_LOCAL_PATH = "~/GoProjects/src/github.com/kaspanet/kasparov/examples/wallet/"
