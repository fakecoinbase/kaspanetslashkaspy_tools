from kaspy_tools.kaspad import json_rpc_client

def wait_for_kaspad_to_become_active():
    res = json_rpc_client.get_block_template()
    pass

