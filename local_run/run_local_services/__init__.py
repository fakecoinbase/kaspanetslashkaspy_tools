import os
from kaspy_tools import kaspy_tools_constants
import subprocess

def validate_volumes_dir():
    # os.makedirs(kaspy_tools_constants.VOLUMES_DIR_PATH, mode=0o775, exist_ok=True)
    # os.makedirs(kaspy_tools_constants.VOLUMES_DIR_PATH + '/kaspad', mode=0o775, exist_ok=True)
    # os.makedirs(kaspy_tools_constants.VOLUMES_DIR_PATH + '/build', mode=0o775, exist_ok=True)

    vol_dir = kaspy_tools_constants.VOLUMES_DIR_PATH
    kaspd_dir = kaspy_tools_constants.VOLUMES_DIR_PATH + '/kaspad'
    build_dir = kaspy_tools_constants.VOLUMES_DIR_PATH + '/build'

    completed_process = subprocess.run(args=['sudo', '-S', 'mkdir',  vol_dir], capture_output=True,
                                       input=kaspy_tools_constants.SUDO_PASSWORD, encoding='utf-8',
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')

    completed_process = subprocess.run(args=['sudo', '-S', 'mkdir',  kaspd_dir], capture_output=True,
                                       input=kaspy_tools_constants.SUDO_PASSWORD, encoding='utf-8',
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')

    completed_process = subprocess.run(args=['sudo', '-S', 'mkdir',  build_dir], capture_output=True,
                                       input=kaspy_tools_constants.SUDO_PASSWORD, encoding='utf-8',
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')

validate_volumes_dir()
