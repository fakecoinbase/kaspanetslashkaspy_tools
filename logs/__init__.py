import os
from kaspy_tools import kaspy_tools_constants

def vlidate_logs_dir():
    os.makedirs(kaspy_tools_constants.LOGS_DIR_PATH, mode=0o775, exist_ok=True)


vlidate_logs_dir()
