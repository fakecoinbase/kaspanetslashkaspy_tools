import os
import shutil
import json
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.logs import config_logger
from kaspy_tools.kaspy_tools_constants import VOLUMES_DIR_PATH

KT_logger = config_logger.get_kaspy_tools_logger()


def save_volume_files(*, work_dir, dag_dir, miner_address):
    """
    Copy the content of volumes/kaspad directory into another directory.
    The main use is to enavle saving of DAGS after creating them.
    :param dir_name: The directory to copy to
    :return:
    """
    dagdir = VOLUMES_DIR_PATH + '/' + dag_dir
    workdir = VOLUMES_DIR_PATH + '/' + work_dir
    shutil.copytree(dagdir, workdir, dirs_exist_ok=True)
    KT_logger.debug('Copied: "{}", to: "{}"'.format(dagdir, workdir))
    save_miner_address(miner_address=miner_address, dir_name=dag_dir)


def restore_volume_files(*, dag_dir, work_dir='kaspad'):
    """
    Restore files from a backup directory into volumes/kaspad
    Main use:
    To restore an already created DAG into kaspad.
    :param dir_name: The directory to restore from.
    :return: None
    """
    dagdir = VOLUMES_DIR_PATH + '/' + dag_dir
    workdir = VOLUMES_DIR_PATH + '/' + work_dir
    shutil.rmtree(workdir)
    shutil.copytree(dagdir, workdir, dirs_exist_ok=True)
    KT_logger.debug('Copied: "{}", to: "{}"'.format(dagdir, workdir))


def volume_dir_exist(volume_dir_name):
    """
    Check weather a volumes dir (directory under the 'volumes' dir) exists.
    :param volume_dir_name: The name of the volume directory.
    :return: bool
    """
    volume_dir = os.path.expanduser(kaspy_tools_constants.VOLUMES_DIR_PATH)
    files = os.listdir(volume_dir)
    return volume_dir_name in files


def save_miner_address(*, miner_address, dir_name):
    """
    Save a miner address of a DAG.
    :param miner_address: A private (wif encoded) address
    :param dir_name: A directory that contains the DAG matching this address (under VOLUMES directory)
    :return: None
    """
    try:
        with open(VOLUMES_DIR_PATH + '/miner_addresses.json', 'r') as addrs_file:
            mining_addresses = json.load(addrs_file)
    except FileNotFoundError:
        mining_addresses = {}

    mining_addresses[dir_name] = miner_address.get_wif()
    with open(VOLUMES_DIR_PATH + '/miner_addresses.json', 'w') as addrs_file:
        json.dump(mining_addresses, addrs_file)


def load_miner_address(*, dir_name):
    with open(VOLUMES_DIR_PATH + '/miner_addresses.json', 'r') as addrs_file:
        mining_addresses = json.load(addrs_file)

    addr = KaspaAddress(wif=mining_addresses[dir_name])
    return addr
