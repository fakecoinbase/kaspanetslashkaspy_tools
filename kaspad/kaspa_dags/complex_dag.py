from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress
from kaspy_tools.kaspad.kaspa_dags.dag_tools import chains_dag
from kaspy_tools.kaspad.kaspa_dags.dag_tools import save_restore_dags
from kaspy_tools.local_run.run_local_services import run_services


def get_complex_dag(*, conn):
    if not save_restore_dags.volume_dir_exist('complex'):
        addr = make_complex_dag(conn=conn)
        run_services.docker_compose_stop('kaspad-first', 'kaspad-second')
        run_services.stop_and_remove_all_runners()
        save_restore_dags.save_volume_files(dag_dir="complex", work_dir='kaspad', miner_address=addr)
        run_services.run_kaspanet_services()  # no kasparov
    else:
        run_services.docker_compose_stop('kaspad-first', 'kaspad-second')
        run_services.docker_compose_rm('kaspad-first', 'kaspad-second')
        save_restore_dags.restore_volume_files(dag_dir='complex', work_dir='kaspad')
        run_services.run_kaspanet_services()


def make_complex_dag(conn):
    miner_addr = KaspaAddress()
    chain_one = chains_dag.get_blocks_from_chain(chain_definition=[1] * 110, pay_address=miner_addr,
                                                 conn=conn)
    # when we get the blocks for chain_two, we clean blocks of chain_one
    chain_two = chains_dag.get_blocks_from_chain(chain_definition=[3, 1], conn=conn, pay_address=miner_addr,
                                                 clear=False)
    # Now chain_two is submitted, we submit chain_one
    chains_dag.submit_saved_blocks(saved_blocks=chain_one, conn=conn)
    # Now chain_one AND chain_two are submitted
    # getting chain_three without clearing:
    chain_three = chains_dag.get_blocks_from_chain(chain_definition=[1 for i in range(110)], clear=False,
                                                   pay_address=miner_addr, conn=conn)
    # now submit
    return miner_addr
