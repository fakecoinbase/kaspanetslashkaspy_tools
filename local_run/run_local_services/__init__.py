import os
from kaspy_tools import kaspy_tools_constants

def vlidate_volumes_dir():
    os.makedirs(kaspy_tools_constants.VOLUMES_DIR_PATH, mode=0o775, exist_ok=True)


vlidate_volumes_dir()
