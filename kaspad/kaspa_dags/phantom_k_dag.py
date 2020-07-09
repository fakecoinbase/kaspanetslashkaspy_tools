from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.kaspad.kaspa_dags.dag_tools import chains_dag
from kaspy_tools.kaspad.kaspa_dags.dag_tools import save_restore_dags
from kaspy_tools.local_run.run_local_services import run_services

PHANTOM_K_DAG_SIZE = 1000 + 10

def get_phantom_k_dag(*, conn):
    if not save_restore_dags.volume_dir_exist('phantomk_dag'):
        addr = make_phantom_k_dag(conn=conn)
        run_services.stop_docker_compose_services('kaspad-first', 'kaspad-second')
        run_services.stop_and_remove_all_runners()
        save_restore_dags.save_volume_files(dag_dir="phantomk_dag", work_dir='kaspad', miner_address=addr)
        run_services.run_kaspanet_services()  # no kasparov
    else:
        run_services.stop_docker_compose_services('kaspad-first', 'kaspad-second')
        run_services.docker_compose_rm('kaspad-first', 'kaspad-second')
        save_restore_dags.restore_volume_files(dag_dir='phantomk_dag', work_dir='kaspad')
        run_services.run_kaspanet_services()


def make_phantom_k_dag(conn):
    miner_addr = KaspaAddress()
    chain_one = chains_dag.get_blocks_from_chain(chain_definition=[1] * PHANTOM_K_DAG_SIZE, pay_address=miner_addr,
                                                 conn=conn, clear=False)
    return miner_addr
