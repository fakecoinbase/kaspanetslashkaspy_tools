"""
run_services module can be used to run kaspanet containers of all kinds.
Building the docker images is done elsewhere.
"""
import os
import time
import subprocess
import shutil
from pathlib import Path
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.local_run.run_services import docker_compose_utils
from kaspy_tools.kaspy_tools_constants import VOLUMES_DIR_PATH
from kaspy_tools.logs import config_logger

KT_logger = config_logger.get_kaspy_tools_logger()


def run_services(run_kasparov=False):
    """
    Run services from docker-compose.yaml
    :param run_kasparov: weather or not to run kasparov services
    :return: A dictionary with service connections
    """
    if not docker_compose_utils.docker_compose_file_exist():
        mining_address = docker_compose_utils.get_mining_address()
        docker_compose_utils.create_docker_compose_file(mining_address)

    docker_compose_data = docker_compose_utils.read_docker_compose_file()
    cons = docker_compose_utils.get_cons_from_docker_compose(docker_compose_data)
    run_docker_compose('kaspad-first', 'kaspad-second')
    if run_kasparov == True:
        run_docker_compose('db')
        run_docker_compose('kasparov_migrate', detached=False)
        run_docker_compose('kasparovsyncd')
        run_docker_compose('kasparovd')
    return cons


def run_docker_compose(*services, detached=True):
    """
    General tool to run services from the docker-compose.yaml
    :param services: an iterable of service names (strings)
    :param detached: Weather or not to block until containers stop
    :return: None
    """
    cmd_args = []
    cmd_args.extend(['docker-compose', 'up'])
    if detached:
        cmd_args.append('-d')
    cmd_args.extend(services)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    time.sleep(2)


def stop_docker_compose_services(*services):
    """
    General tool to run services from the docker-compose.yaml
    :param services: an iterable of service names (strings)
    :param detached: Weather or not to block until containers stop
    :return: None
    """
    cmd_args = []
    cmd_args.extend(['docker-compose', 'down'])
    if services is not None:
        cmd_args.extend(services)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    time.sleep(2)


def volume_dir_exist(volume_dir_name):
    volume_dir = os.path.expanduser(kaspy_tools_constants.VOLUMES_DIR_PATH)
    files = os.listdir(volume_dir)
    return volume_dir_name in files


def clear_volume_files():
    volume_kaspad = VOLUMES_DIR_PATH + '/kaspad'
    if Path(volume_kaspad).exists():
        shutil.rmtree(volume_kaspad)
        os.mkdir(volume_kaspad)
    else:
        os.makedirs(volume_kaspad)
        KT_logger.debug("Created: " + volume_kaspad)


def save_volume_files(*, dir_name):
    src = VOLUMES_DIR_PATH + '/kaspad'
    dst = VOLUMES_DIR_PATH + '/' + dir_name
    shutil.copytree(src, dst, dirs_exist_ok=True)
    KT_logger.debug('Copied: "{}", to: "{}"'.format(src, dst))


def restore_volume_files(*, dir_name):
    clear_volume_files()
    src = VOLUMES_DIR_PATH + '/' + dir_name
    dst = VOLUMES_DIR_PATH + '/kaspad'
    shutil.copytree(src, dst, dirs_exist_ok=True)
    KT_logger.debug('Copied: "{}", to: "{}"'.format(src, dst))

def get_all_containers():
    """
    Finds all container (both stopped and running)
    :return: All container ids as a list
    """
    cmd_args = []
    cmd_args.extend(['docker', 'ps', '-a', '-q'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    containers = completed_process.stdout.split()
    return containers

def remove_all_containers():
    """
    Removes all containers.
    :return: None
    """
    containers = get_all_containers()
    if not containers:
        return
    cmd_args = []
    cmd_args.extend(['docker', 'rm', '-f'])
    cmd_args.extend(containers)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


if __name__ == "__main__":
    run_services(run_kasparov=True)
    # remove_all_containers()