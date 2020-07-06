from _datetime import datetime
import time
from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.kaspad.kaspa_dags.dag_tools import dag_make, save_restore_dags
from kaspy_tools.local_run.run_local_services import run_services, docker_compose_utils
from kaspy_tools.kaspad.json_rpc import json_rpc_requests

big_dag_block_count = 1000
very_big_dag_dir = 'very_big_dag'
very_big_work_dir = 'build'
use_dir = 'kaspad'

def get_big_dag(*, block_count=big_dag_block_count):
    if not save_restore_dags.volume_dir_exist(very_big_dag_dir):
        generate_very_big_dag(block_count=big_dag_block_count)
    else:
        run_services.stop_docker_compose_services('kaspad-builder-1', 'kaspad-builder-2')
        run_services.docker_compose_rm('kaspad-builder-1', 'kaspad-builder-2')
        save_restore_dags.restore_volume_files(dag_dir=very_big_dag_dir, work_dir=use_dir)


def generate_very_big_dag(*, block_count):
    miner_addr = KaspaAddress()
    run_services.stop_docker_compose_services('kaspad-builder-1', 'kaspad-builder-2')
    run_services.docker_compose_rm('kaspad-builder-1', 'kaspad-builder-2')
    save_restore_dags.clear_dag_files(work_dir=very_big_work_dir, dag_dir=very_big_dag_dir)
    run_services.run_docker_compose('kaspad-builder-1', 'kaspad-builder-2')
    time.sleep(5)
    docker_compose_data = docker_compose_utils.read_docker_compose_file()
    conn = docker_compose_utils.get_cons_from_docker_compose(docker_compose_data)['kaspad-builder-1']
    current_blocks_count = json_rpc_requests.get_block_dag_info_request(conn=conn)['result']['blocks']
    t0 = datetime.now()
    while current_blocks_count < block_count:
        dag_make.make_dag(floors=500, min_width=1, max_width=1, conn=conn)
        current_blocks_count = json_rpc_requests.get_block_dag_info_request(conn=conn)['result']['blocks']
        t_now = datetime.now()
        print(f'blocks: {current_blocks_count} time: {t_now-t0}')
    current_blocks_count = json_rpc_requests.get_block_dag_info_request(conn=conn)['result']['blocks']
    run_services.stop_docker_compose_services('kaspad-builder-1', 'kaspad-builder-2')
    run_services.docker_compose_rm('kaspad-builder-1', 'kaspad-builder-2')
    save_restore_dags.save_volume_files(dag_dir=very_big_dag_dir, work_dir=very_big_work_dir, miner_address=miner_addr)
    return miner_addr


if __name__ == '__main__':
    run_services.stop_docker_compose_services('kaspad-builder-1', 'kaspad-builder-2')
    run_services.docker_compose_rm('kaspad-builder-1', 'kaspad-builder-2')
    save_restore_dags.clear_dag_files(work_dir=very_big_work_dir, dag_dir=very_big_dag_dir)
    generate_very_big_dag(block_count=big_dag_block_count)