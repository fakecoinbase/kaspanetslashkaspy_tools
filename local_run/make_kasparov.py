from kaspy_tools import kaspy_tools_constants
from kaspy_tools.local_run import build_common

kasparov_branch = 'v0.4.1-dev'


def build_and_tag_kasparov_services():
    kasparov_sync_dir = kaspy_tools_constants.LOCAL_RUN_PATH + '/kasparov_docker/kasparov_sync'
    kasparov_daemon_dir = kaspy_tools_constants.LOCAL_RUN_PATH + '/kasparov_docker/kasparovd'
    commit_number = build_common.get_git_commit(kaspy_tools_constants.KASPAROV_TOP_PATH, kasparov_branch)
    build_common.build_image(service_name='kasparov-sync', build_dir=kasparov_sync_dir,
                             extra_parameter='KASPAD_VERSION=' + kasparov_branch,
                             commit_number=commit_number,
                             context_dir= kaspy_tools_constants.KASPAROV_TOP_PATH)
    build_common.build_image(service_name='kasparovd', build_dir=kasparov_daemon_dir,
                             extra_parameter='KASPAD_VERSION=' + kasparov_branch,
                             commit_number=commit_number,
                             context_dir=kaspy_tools_constants.KASPAROV_TOP_PATH)
    build_common.tag_service('kasparov-sync', commit_number)
    build_common.tag_service('kasparovd', commit_number)


if __name__ == "__main__":
    build_and_tag_kasparov_services()
