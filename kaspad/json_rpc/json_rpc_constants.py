"""
This file holds all the constant elements that are being used by the JSON-RPC automation.
"""
import os

# Path for the local certification file
CERT_FILE_PATH = os.path.expanduser("~/kaspanet/automation_testing/cert_files/rpc.cert")

# The port number depends on the one written in the .conf file
RPC_PORT = 16610

# The RPC username and RPC password MUST match the one in the .conf file
RPC_USER = 'user'
RPC_PASSWORD = 'pass'

# The KASPAROV_URL to be used
RPC_DEVNET_URL = "https://" + RPC_USER + ":" + RPC_PASSWORD + "@btcd-0.daglabs.com" + ":" + str(RPC_PORT)

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
