import os
from pathlib import Path

# Path for the top go directory
KASPAD_TOP_PATH = os.path.expanduser("~/GoProjects/src/github.com/kaspanet/kaspad")

# Path for the top kaspy directory
KASPY_TOOLS_PATH = str(Path(__file__).parent.absolute())

# Path for the local_run folder
LOCAL_RUN_PATH = KASPY_TOOLS_PATH + "/local_run"

# Path for graph images
GRAPH_IMAGES_PATH = KASPY_TOOLS_PATH + "/kaspad/kaspa_dags/graph_images"

# Path for the local certification file
CERT_FILE_PATH = os.path.expanduser("~/GoProjects/src/github.com/kaspanet/automation_testing/cert_files/rpc.cert")

# Path for the local certification file
VOLUMES_DIR_PATH = os.path.expanduser("~/volumes")

# Path for the local certification file
LOGS_DIR_PATH = os.path.expanduser("/var/logs/")
