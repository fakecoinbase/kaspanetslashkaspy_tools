"""
run_local_services module can be used to run kaspanet containers.
We can run 2 kinds of nodes:
  runners - nodes that are run for tests (kaspad-first, kaspad-second, kaspad-third, kaspad-forth, kaspad-fifth)
  builders - nodes that mine blocks for nig DAGs (kaspad-builder-1, kaspad-builder-2)
"""
import time
import subprocess
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspad.json_rpc import json_rpc_requests
from kaspy_tools.kaspad.kaspa_dags.dag_tools import save_restore_dags
from kaspy_tools.local_run.run_local_services import docker_compose_utils
from kaspy_tools.logs import config_logger

KT_logger = config_logger.get_kaspy_tools_logger()


def run_kaspanet_services(run_kasparov=False):
    """
    Run services from docker-compose.yaml (which is built automatically from docker-compose-template.yaml)
    Runs:
     - a pair of connected kaspad services
     - kasparov services: kasparov_migrate, kasparovd, kasparov-sync, postgres db,
    :param run_kasparov: weather or not to run also the kasparov services.
    :return: A dictionary with service connections
    """
    if not docker_compose_utils.docker_compose_file_exist():
        docker_compose_utils.create_docker_compose_file()

    docker_compose_data = docker_compose_utils.read_docker_compose_file()
    cons = docker_compose_utils.get_cons_from_docker_compose()
    run_docker_compose('kaspad-first', 'kaspad-second')
    if run_kasparov == True:
        run_docker_compose('db')
        run_docker_compose('kasparov_migrate', detached=False)
        run_docker_compose('kasparovsyncd')
        run_docker_compose('kasparovd')
    time.sleep(5)  # let services start
    return cons


def run_docker_compose(*services, detached=True, kaspanet='devnet'):
    """
    General tool to run services from the docker-compose.yaml
    :param services: an iterable of service names (strings)
    :param detached: Weather or not to block until containers stop
    :return: None
    """
    docker_compose_utils.set_compose_network(*services, kaspanet=kaspanet)
    cmd_args = []
    cmd_args.extend(['docker-compose', 'up'])
    if detached:
        cmd_args.append('-d')
    cmd_args.extend(services)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    cons = docker_compose_utils.get_cons_from_docker_compose()
    if kaspanet == 'devnet':
        wait_for_node(conn=cons[services[0]], netprefix='kaspadev')
    elif kaspanet == 'simnet':
        wait_for_node(conn=cons[services[0]], netprefix='kaspasim')


def wait_for_node(*, conn, netprefix):
    ready_to_start=False
    count=0
    while not ready_to_start:
        try:
            template = json_rpc_requests.get_block_template_request(conn=conn,  netprefix=netprefix)
        except:
            time.sleep(1)  # do not try too often
            continue
        if template['result'] != None:
            KT_logger.info('Kaspa is ready: %s', str(template['result'])[:60])
            ready_to_start = True
            break
        KT_logger.warning('Kaspa is not ready yet: %s', str(template['error'])[:60])
        count += 1
        time.sleep(1)   # do not try too often

def hard_restart_docker_compose(*services, clear_dir='kaspad', kaspanet='devnet'):
    stop_docker_compose_services(services)
    docker_compose_rm(*services)
    if clear_dir:
        save_restore_dags.clear_dag_files(work_dir=clear_dir)
    run_docker_compose(*services, kaspanet=kaspanet)


def stop_docker_compose_services(*services):
    """
    General tool to stop services from the docker-compose.yaml
    :param services: an iterable of service names (strings) to stop
    :return: None
    """
    containers = get_all_runner_containers_ids()
    cmd_args = []
    cmd_args.extend(['docker-compose', 'stop'])
    # if services is not None:
    #     cmd_args.extend(services)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


def node_synced(*, cons, netprefix):
    for conn in cons:
        sync_status = json_rpc_requests.get_block_template_request(conn=conn,
                                                                         netprefix='kaspasim')['result']['isSynced']
        if sync_status == False:
            return False
    else:
        return True

def docker_compose_rm(*services):
    """
     General tool to remove stopped container
     :param services: an iterable of service names (strings) to remove
     :return: None
     """
    cmd_args = []
    cmd_args.extend(['docker-compose', 'rm', '-f'])
    if services is not None:
        cmd_args.extend(services)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


def get_all_runner_containers_ids():
    """
    Finds all containers (both stopped and running) that were created by local_run code.
    :return: All container ids as a list
    """
    cmd_args = []
    cmd_args.extend(['docker', 'ps', '-a', '-q', '-f', 'name=localrun'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')

    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0
    containers = completed_process.stdout.split()
    return containers


def stop_and_remove_all_runners():
    """
    Stop and removes all 'runner' containers created by local_run code.
    :return: None
    """
    containers = get_all_runner_containers_ids()
    if not containers:
        return
    cmd_args = []
    cmd_args.extend(['docker', 'rm', '-f'])
    cmd_args.extend(containers)
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       cwd=kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services')
    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


if __name__ == "__main__":
    run_kaspanet_services(run_kasparov=True)
    # stop_and_remove_all_runners()
