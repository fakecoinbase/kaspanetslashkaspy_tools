"""
This file holds all the constant elements that are being used by the JSON-RPC automation.
"""
import os

# Path for the local certification file
CERT_FILE_PATH = os.path.expanduser("~/PycharmProjects/automation/cert_files/rpc.cert")

# Path for the binary file of a valid empty block
VALID_BLOCK_EMPTY_PATH = os.path.expanduser("~/PycharmProjects/automation/blocks/Blocks_Cartridge/valid_block_empty.dat")

# Path for the binary file of valid 1848 block
VALID_1848_BLOCKS_PATH = os.path.expanduser("~/PycharmProjects/automation/blocks/Blocks_Cartridge/1848_blocks.dat")

# Path for the binary file of valid 2138 block
VALID_2138_BLOCKS_PATH = os.path.expanduser("~/PycharmProjects/automation/blocks/Blocks_Cartridge/2138_blocks.dat")

# Path for the local KASPAD folder
KASPAD_LOCAL_PATH = os.path.expanduser("~/GoProjects/src/github.com/kaspanet/kaspad")

# Path for the local run-dev folder
RUNDEV_LOCAL_PATH = os.path.expanduser("~/GoProjects/src/github.com/kaspanet/stuff/run-dev")

# The port number depends on the one written in the .conf file
RPC_PORT = 16610

# The RPC username and RPC password MUST match the one in the .conf file
RPC_USER = 'user'
RPC_PASSWORD = 'pass'

# The KASPAROV_URL to be used
RPC_DEVNET_URL = "https://" + RPC_USER + ":" + RPC_PASSWORD + "@btcd-0.daglabs.com" + ":" + str(RPC_PORT)

# The max value possible of uint64
MAX_UINT64 = 0xffffffffffffffff

# Hash of Genesis block (devnet)
GENESIS_HASH = "000033abb09b45e09ef5e3a2b92185b7503a074565ef5706904167c60b37d6f4"
# GENESIS_HASH = "f4d6370bc66741900657ef6545073a50b78521b9a2e3f59ee0459bb0ab330000"

# Finality value (devnet)
FINALITY_DEVNET = 1000

# Phantom K
PHANTOM_K = 10

# Local nodes
# LOCAL_NODE_1 = "https://" + RPC_USER + ":" + RPC_PASSWORD + "@127.0.0.1:18334"
# LOCAL_NODE_2 = "https://" + RPC_USER + ":" + RPC_PASSWORD + "@127.0.0.1:18335"
LOCAL_NODE_1 = "http://" + RPC_USER + ":" + RPC_PASSWORD + "@127.0.0.1:16615"
LOCAL_NODE_2 = "http://" + RPC_USER + ":" + RPC_PASSWORD + "@127.0.0.1:16616"

# Local node loading/teardown verification strings
LOCAL_NODE_BUILD_VERIFICATION = ["Successfully", "tagged", "kaspad"]
# LOCAL_NODE_LOAD_VERIFICATION = ["RPC", "server", "listening", "on", "0.0.0.0:18334"]
LOCAL_NODE_LOAD_VERIFICATION = ["New", "valid", "peer", "127.0.0.1"]
LOCAL_NODE_TEARDOWN_VERIFICATION = ["Removing"]
