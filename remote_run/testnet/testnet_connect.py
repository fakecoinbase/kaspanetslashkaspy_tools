import json
import subprocess
import psutil
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspa_model.kaspa_node import KaspaNode

def get_testnet_nodes(*, net_name='testnet'):
    all_nodes = {}
    with open(kaspy_tools_constants.REMOTE_RUN_PATH + '/testnet_nodes.json') as f:
        nodes = json.load(f)
        for node_name, node_details in nodes.items():
            new_kaspa_node = KaspaNode(conn_name=node_name, ip_addr=node_details['ip_addr'],
                                       domain_name=node_details.get('domain'),
                                       port_number=node_details['rpc-port'],
                                       tls=True,username=node_details.get('user'),
                                       password=node_details.get('pass'),
                                       cert_file_path=kaspy_tools_constants.KEYS_PATH + '/' + net_name +\
                                                      '/rpc.cert')
            all_nodes[node_name] = new_kaspa_node

    return all_nodes

def run_openvpn():
    cmd_args = []
    params = 'sudo -S openvpn --config client.ovpn --auth-user-pass login.conf --daemon'.split()
    cmd_args.extend(params)

    input_str = kaspy_tools_constants.SUDO_PASSWORD + kaspy_tools_constants.OPENVPN_USER + kaspy_tools_constants.OPENVPN_PASS
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       input=input_str + '\n',
                                       encoding='utf-8', cwd=kaspy_tools_constants.REMOTE_RUN_PATH)


    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0

def is_openvpn_running():
    openvpn_procs = [psutil.Process(p).pid  for p in psutil.pids() if psutil.Process(p).name() == 'openvpn']
    return (len(openvpn_procs) > 0)

def kill_openvpn_procs():
    openvpn_procs = [str(psutil.Process(p).pid)  for p in psutil.pids() if psutil.Process(p).name() == 'openvpn']
    cmd_args = 'sudo -S kill -9'.split()
    cmd_args.extend(openvpn_procs)

    input_str = kaspy_tools_constants.SUDO_PASSWORD
    completed_process = subprocess.run(args=cmd_args, capture_output=True,
                                       input=input_str + '\n',
                                       encoding='utf-8')

    completed_process.check_returncode()  # raise CalledProcessError if return code is not 0


if __name__ == "__main__":
    run_openvpn()
    all = get_testnet_nodes(net_name='testnet')
    pass
