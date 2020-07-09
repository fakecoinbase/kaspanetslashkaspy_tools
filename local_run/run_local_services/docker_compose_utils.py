"""
A set of utilities to handle docker-compose.
"""
from kaspy_tools import kaspy_tools_constants
import json
import yaml
from kaspy_tools.kaspy_tools_constants import VOLUMES_DIR_PATH
from pathlib import Path
from kaspy_tools.kaspa_model.kaspa_node import KaspaNode


def read_docker_compose_template():
    """
    Read the docker-compose-template.yaml file, and parse it using yaml library.
    :return: yaml parsed data
    """
    docker_file = kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services/docker-compose-template.yaml'
    with open(docker_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def read_docker_compose_file():
    """
    Read the docker-compose.yaml file, and parse it.
    :return: yaml parsed data.
    """
    docker_file = kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services/docker-compose.yaml'
    with open(docker_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def write_docker_compose(yaml_data):
    """
    Create and write the docker-compose.yaml file
    :param yaml_data: Data to write
    :return:
    """
    docker_file = kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services/docker-compose.yaml'
    with open(docker_file, 'w') as f:
        yaml.dump(yaml_data, f)


def create_docker_compose_file():
    """
    Create a new docker-compose.yaml file based on the template, updating stuff in it.
    :return:
    """
    data = read_docker_compose_template()

    command = data['services']['kaspad-first']['command']
    # Replace the keys path in volumes.
    for service in ['kaspad-first', 'kaspad-second']:
        volumes = data['services'][service]['volumes']
        data['services'][service]['volumes'] = [v.replace('KEYS', kaspy_tools_constants.KEYS_PATH) for v in volumes]

    # Write output
    write_docker_compose(yaml_data=data)

def set_compose_network(*service_names, kaspanet):
    data = read_docker_compose_file()
    for srv_name in service_names:
        service = data['services'][srv_name]
        net_index = [i for i in range(len(service['command'])) if 'net' in service['command'][i]][0]
        service['command'][net_index] = '--' + kaspanet

    write_docker_compose(data)


def get_cons_from_docker_compose():
    """
    Read connection data to services defined in docker-compose.yaml file.
    :param docker_compose_data: Data parsed from docker-compose.yaml file.
    :return: A dictionary with services as keys, kaspa_model/kaspa_node as values.
    """
    cons = {}
    docker_compose_data = read_docker_compose_file()
    for srv_name, service in docker_compose_data['services'].items():
        if 'kaspad' not in srv_name:
            continue
        addr_index = [i for i in range(len(service['command'])) if 'rpclisten' in service['command'][i]][0]
        ip_addr, port_num = (service['command'][addr_index].split('=')[1]).split(':')
        if ip_addr == '0.0.0.0':
            ip_addr = '127.0.0.1'   # 0.0.0.0 is good for listening, not for connecting
        user_index = [i for i in range(len(service['command'])) if 'rpcuser' in service['command'][i]][0]
        pass_index = [i for i in range(len(service['command'])) if 'rpcpass' in service['command'][i]][0]
        username = (service['command'][user_index].split('=')[1])
        password = (service['command'][pass_index].split('=')[1])
        cert_file = kaspy_tools_constants.KEYS_PATH + '/rpc.cert'
        new_conn = KaspaNode(conn_name=srv_name, ip_addr=ip_addr, port_number=port_num, tls=True,
                             username=username, password=password, cert_file_path=cert_file)
        cons[srv_name] = new_conn

    return cons


def docker_compose_file_exist():
    """
    Check weather docker-compose.yaml file exists
    :return: bool
    """
    return Path(kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services/docker-compose.yaml').is_file()

def set_localrun_network(*, network_name):
    set_docker_container_network(container_name='kaspad-first', network_name='devnet')
    set_docker_container_network(container_name='kaspad-second', network_name='devnet')
    set_docker_container_network(container_name='kaspad-third', network_name='devnet')
    set_docker_container_network(container_name='kaspad-second', network_name='devnet')
    set_docker_container_network(container_name='kaspad-first', network_name='devnet')


def set_docker_container_network(*, container_name, network_name):
    data = read_docker_compose_file()
    service = data['services'][container_name]
    net_index = [i for i in range(len(service['command'])) if 'net' in service['command'][i]][0]
    service['command'][net_index] = '--' + network_name
    write_docker_compose(data)