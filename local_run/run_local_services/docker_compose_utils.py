"""
A set of utilities to handle docker-compose.
"""
from kaspy_tools import kaspy_tools_constants
import yaml
from pathlib import Path
from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
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


def create_docker_compose_file(mining_address):
    """
    Create a new docker-compose.yaml file based on the template, updating stuff in it.
    Update mining address just for kaspad-first.
    :param mining_address: A KaspaAddress instance based on the private wif saved in file.
    :return:
    """
    save_wif_file = kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services/save_mining'
    data = read_docker_compose_template()

    command = data['services']['kaspad-first']['command']
    addr_index = [i for i in range(len(command)) if 'miningaddr' in command[i]][0]

    old_address = data['services']['kaspad-first']['command'][addr_index]
    parts = old_address.split('=')
    parts[1] = mining_address.get_address("kaspadev")  # replace the old Bech32 with the mining address
    data['services']['kaspad-first']['command'][addr_index] = '='.join(parts)
    # Replace the keys path in volumes.
    for service in ['kaspad-first', 'kaspad-second']:
        volumes = data['services'][service]['volumes']
        data['services'][service]['volumes'] = [v.replace('KEYS', kaspy_tools_constants.KEYS_PATH) for v in volumes]

    # Write Linux UID and GID
    data['services']['kaspad-first']['user'] = '1000:1000'

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
    save_mining = kaspy_tools_constants.LOCAL_RUN_PATH + '/run_local_services/save_mining'
    with open(save_mining) as f:
        wif_data = f.readline()

    mining_address = KaspaAddress(wif_data)
    return mining_address


def get_cons_from_docker_compose(docker_compose_data):
    """
    Read connection data to services defined in docker-compose.yaml file.
    :param docker_compose_data: Data parsed from docker-compose.yaml file.
    :return: A dictionary with services as keys, kaspa_model/kaspa_node as values.
    """
    cons = {}
    for srv_name, service in docker_compose_data['services'].items():
        if srv_name not in ('kaspad-first', 'kaspad-second'):
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
