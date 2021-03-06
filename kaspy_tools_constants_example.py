import os
from pathlib import Path

# Needed to run things as a superuser
SUDO_PASSWORD = 'abcde\n'

# Branhces to get while building kaspad and kasparov
KASPAD_BRANCH = 'v0.6.0-dev'
KASPAROV_BRANCH = 'v0.6.0-dev'


# OpenVpn credentials
OPENVPN_USER = 'david\n'
OPENVPN_PASS = 'dave12345\n'

# Path for the top go directory
KASPANET_TOP_PATH = os.path.expanduser("~/kaspanet")

# Path for the top go directory
KASPAD_TOP_PATH = os.path.expanduser(KASPANET_TOP_PATH + "/kaspad")

# Path for the top kasparov go directory
KASPAROV_TOP_PATH = os.path.expanduser(KASPANET_TOP_PATH + "/kasparov")

# Path for the top kaspy directory
KASPY_TOOLS_PATH = str(Path(__file__).parent.absolute())

# Path for the local_run folder
LOCAL_RUN_PATH = KASPY_TOOLS_PATH + "/local_run"

# Path for the remote_run folder
REMOTE_RUN_PATH = KASPY_TOOLS_PATH + "/remote_run"

# Path for graph images
GRAPH_IMAGES_PATH = KASPY_TOOLS_PATH + "/kaspad/kaspa_dags/graph_images"

# Path for the volumes directory (docker)
VOLUMES_DIR_PATH = os.path.expanduser(KASPY_TOOLS_PATH + "/local_run/run_local_services/volumes")

# Path for the logs directory
LOGS_DIR_PATH = os.path.expanduser(KASPY_TOOLS_PATH + "/logs/files")

# Path for certificates (rpc.key and rpc.cert)
KEYS_PATH = os.path.expanduser(LOCAL_RUN_PATH + "/run_local_services/keys")

# Default fees to use when creating transactions
DEFAULT_FEE = 1000000

# Maximum number to use for blocks retrieval in tests
MAX_BLOCKS_IN_TESTS = 1000

# Timeout for requests connection
REQUEST_TIMEOUT = 100   # seconds

# AWS api key_id and secret kay value
AWS_ACCESS_KEY_ID='mykey'
AWS_SECRET_ACCESS_KEY='sdhflkgshdflks'
