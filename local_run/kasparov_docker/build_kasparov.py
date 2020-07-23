"""
Build images for kasparov.
"""
import sys
import subprocess
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.local_run import build_common
from kaspy_tools.logs import config_logger

KT_logger = config_logger.get_kaspy_tools_logger()


def build_and_tag_kasparov_services():
    """
    Build and tag the kasparov images.
    :return:
    """
    try:
        kasparov_branch = sys.argv[1]
    except:
        kasparov_branch = kaspy_tools_constants.KASPAROV_BRANCH


    KT_logger.info('Started building kasparov-sync image(s).')
    kasparov_sync_dir = kaspy_tools_constants.LOCAL_RUN_PATH + '/kasparov_docker/kasparov_sync'
    kasparov_daemon_dir = kaspy_tools_constants.LOCAL_RUN_PATH + '/kasparov_docker/kasparovd'
    commit_number = build_common.get_git_commit(kaspy_tools_constants.KASPAROV_TOP_PATH, kasparov_branch)
    build_common.build_image(service_name='kasparov-sync', build_dir=kasparov_sync_dir,
                             extra_parameter='KASPAD_VERSION=' + kasparov_branch,
                             commit_number=commit_number,
                             context_dir= kaspy_tools_constants.KASPAROV_TOP_PATH)
    KT_logger.info('Finished building kasparov-sync image(s).')

    KT_logger.info('Started building kasparovd image(s).')
    build_common.build_image(service_name='kasparovd', build_dir=kasparov_daemon_dir,
                             extra_parameter='KASPAD_VERSION=' + kasparov_branch,
                             commit_number=commit_number,
                             context_dir=kaspy_tools_constants.KASPAROV_TOP_PATH)
    build_common.tag_service('kasparov-sync', commit_number)
    build_common.tag_service('kasparovd', commit_number)
    KT_logger.info('Finished building kasparovd image(s).')

def pull_postgres_image():
    KT_logger.info('Started pulling postgres image.')
    cmd_args = []
    cmd_args.extend(['docker', 'pull', 'postgres'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)
    if completed_process.returncode != 0:
        print(completed_process.stderr)
    completed_process.check_returncode()
    KT_logger.info('Finished pulling postgres image.')

if __name__ == "__main__":
    build_and_tag_kasparov_services()
