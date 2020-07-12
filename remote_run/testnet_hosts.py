import json
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspa_model.kaspa_node import KaspaNode

def get_testnet_nodes(*, net_name='testnet'):
    all_nodes = {}
    with open(kaspy_tools_constants.REMOTE_RUN_PATH + '/testnet_nodes.json') as f:
        nodes = json.load(f)
        for node_name, node_details in nodes.items():
            new_kaspa_node = KaspaNode(conn_name=node_name, ip_addr=node_details['ip_addr'],
                                       port_number=node_details['rpc-port'],
                                       tls=True,
                                       cert_file_path=kaspy_tools_constants.KEYS_PATH + '/' + net_name)
            all_nodes[node_name] = new_kaspa_node

    return all_nodes

if __name__ == "__main__":
    all = get_testnet_node(net_name='testnet')
    pass
