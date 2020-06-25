from kaspy_tools.kaspad.kaspa_dags import chains_dag, dag_make
from kaspy_tools.local_run.run_local_services import run_services, docker_compose_utils
from kaspy_tools.kaspad.json_rpc import json_rpc_requests

def generate_very_big_dag(*, block_count):
    run_services.docker_compose_stop('kaspad-builder-1', 'kaspad-builder-2')
    run_services.docker_compose_rm('kaspad-builder-1', 'kaspad-builder-2')
    run_services.run_docker_compose('kaspad-builder-1', 'kaspad-builder-2')
    docker_compose_data = docker_compose_utils.read_docker_compose_file()
    conns = docker_compose_utils.get_cons_from_docker_compose(docker_compose_data)
    current_blocks_count = json_rpc_requests.get_block_dag_info_request(conn=conn)['result']['blocks']
    while current_blocks_count < block_count:
        dag_make.make_dag(floors=500, min_width=1, max_width=1, conn=conn)
    current_blocks_count = json_rpc_requests.get_block_dag_info_request(conn=conn)['result']['blocks']
    pass

if __name__ == '__main__':
    generate_very_big_dag(block_count=1000)