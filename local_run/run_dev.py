"""
run_dev module can be used to build kaspad iamge and run containers based on it.
A Dockerfile is used to build the kaspad image.
A docker-compose.yaml file is used to run containers.
"""
import os
import time
import subprocess
import yaml
from kaspy_tools.kaspad.json_rpc import json_rpc_constants
from kaspy_tools.kaspy_tools_constants import LOCAL_RUN_PATH
from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.kaspa_model.kaspa_node import KaspaNode

from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspad import kaspad_constants


def read_docker_compose():
    docker_file = LOCAL_RUN_PATH + '/docker_files/docker-compose.yml'
    with open(docker_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

def write_docker_compose(yaml_data):
    docker_file = LOCAL_RUN_PATH + '/docker_files/docker-compose.yml'
    with open(docker_file, 'w') as f:
        yaml.dump(yaml_data, f)


def create_docker_compose_file(mining_address):
    """

    :param address:
    :return:
    """
    save_wif_file = LOCAL_RUN_PATH + '/docker_files/save_mining'
    data = read_docker_compose()

    old_address = data['services']['first']['command'][4]
    parts = old_address.split('=')
    parts[1] = mining_address.get_address("kaspadev")
    data['services']['first']['command'][4] = '='.join(parts)
    # Write output
    write_docker_compose(yaml_data=data)
    with open(save_wif_file, 'w') as mining_f:
        mining_f.write(mining_address.get_wif())


def get_mining_address():
    """
    Restore the mining address from the save_mining file, where the private key is stored
    in wif format.
    :return: The kaspa address object
    """
    save_mining = LOCAL_RUN_PATH + '/docker_files/save_mining'
    with open(save_mining) as f:
        wif_data = f.readline()

    mining_address = KaspaAddress(wif_data)
    return mining_address



def remove_all_images_and_containers():
    """
    Remove all containers and all images from your computer!!!
    Use carefully.
    :return: None
    """
    remove_all_containers()
    cmd_args = []
    cmd_args.extend(['docker', 'system', 'prune', '-f', '-a'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()    # raise CalledProcessError if return code is not 0


def get_all_containers():
    """
    Finds all container (both stopped and running)
    :return: All container ids as a list
    """
    cmd_args = []
    cmd_args.extend(['docker', 'ps', '-a', '-q'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()    # raise CalledProcessError if return code is not 0
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
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()    # raise CalledProcessError if return code is not 0


def run_kaspad_services(debug=False):
    """
    Run 'first' and 'second' of 'second-debug' services from docker-compose.yaml
    :param debug: weather or not to run a debug version of the 2nd service
    :return: A list with the connections
    """
    cons = {}
    data = read_docker_compose()
    for srv_name,service in data['services'].items():
        addr_index = [i for i in range(len(service['command'])) if 'rpclisten' in service['command'][i]][0]
        ip_addr, port_num = (service['command'][addr_index].split('=')[1]).split(':')
        user_index = [i for i in range(len(service['command'])) if 'rpcuser' in service['command'][i]][0]
        pass_index = [i for i in range(len(service['command'])) if 'rpcpass' in service['command'][i]][0]
        username = (service['command'][user_index].split('=')[1])
        password = (service['command'][pass_index].split('=')[1])
        cert_file = json_rpc_constants.CERT_FILE_PATH
        new_conn = KaspaNode(conn_name=srv_name, ip_addr= ip_addr, port_number=port_num, tls=True,
                             username=username, password=password, cert_file_path=cert_file)
        cons[srv_name] =  new_conn


    os.chdir(kaspy_tools_constants.LOCAL_RUN_PATH + '/docker_files')
    if debug:
        second = 'second-debug'
    else:
        second = 'second'
    run_docker_compose_services('first', second)
    return cons

def run_docker_compose_services(*services, detached=True):
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
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()    # raise CalledProcessError if return code is not 0
    time.sleep(2)

def get_git_commit():
    """
    Get the commit id of HEAD  (just first 12 characters)
    :return: a string with the commit id
    """
    completed_process = subprocess.run(args=['git', 'rev-parse', '--short=12', 'HEAD'], capture_output=True)
    completed_process.check_returncode()    # raise CalledProcessError if return code is not 0
    git_commit=completed_process.stdout
    return git_commit.decode('utf-8')[:-1]  # remove \n from the end


def docker_image_build(service_name, context):
    """
    Build a docker image for a service (kaspad, kasparov...)
    :param service_name: kaspad, kasparov... etc
    :param context: context path for Dockerfile command
    :return: None
    """
    os.chdir(kaspy_tools_constants.LOCAL_RUN_PATH)      # go to directory where docker_files are located
    cmd_args = []
    git_commit = get_git_commit()
    cmd_args.extend(['docker', 'build', '-t'])
    cmd_args.extend([service_name + ':' + git_commit, context])
    cmd_args.extend(['-f', 'docker_files/Dockerfile'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)  # command return non-zero good result
    pass


def tag_image_latest(service_name):
    """
    Add a docker 'latest' tag  to the image that was built for this service.
    :param service_name:
    :return: None
    """
    cmd_args = []
    git_commit = get_git_commit()
    cmd_args.extend(['docker', 'tag'])
    cmd_args.extend([service_name + ':' + git_commit])
    cmd_args.extend([service_name + ':' + 'latest'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    completed_process.check_returncode()    # raise CalledProcessError if return code is not 0


# def build_and_run():
#     """
#     An example function, to show how to build image and run a pair of kaspad containers.
#     :return:
#     """
#     os.chdir(kaspy_tools_constants.LOCAL_RUN_PATH)      # go to directory where docker_files are located
#     try:
#         remove_all_images_and_containers()
#         docker_image_build('kaspad', kaspad_constants.KASPAD_LOCAL_PATH)
#         tag_image_latest('kaspad')
#         run_kaspad_services()
#     except subprocess.CalledProcessError as pe:
#         print(pe.stderr)


def clear_volume_files():
    import subprocess
    volume_dir = os.path.expanduser('~/volumes/kaspad')
    cmd2 = subprocess.run(['sudo -S rm -rf *'],capture_output=True, input=b'yuval\x0d', shell=True, cwd=volume_dir)



if __name__ == '__main__':
    create_docker_compose_file(KaspaAddress())
