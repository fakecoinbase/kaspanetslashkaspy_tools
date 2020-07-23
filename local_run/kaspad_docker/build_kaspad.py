import sys
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.local_run import build_common
from kaspy_tools.logs import config_logger

KT_logger = config_logger.get_kaspy_tools_logger()

def build_and_tag_kaspad_image():
    """
    Generates a build to be used by the setUpClass() method of the test-kits.
    """
    try:
        desired_branch = sys.argv[1]
    except:
        desired_branch = kaspy_tools_constants.KASPAD_BRANCH

    KT_logger.info('Started building kaspad image(s).')
    commit_number = build_common.get_git_commit(kaspy_tools_constants.KASPAD_TOP_PATH, branch=desired_branch)
    build_dir = kaspy_tools_constants.LOCAL_RUN_PATH + '/kaspad_docker'
    build_common.build_image(service_name='kaspad', build_dir=build_dir, commit_number=commit_number,
                             context_dir=kaspy_tools_constants.KASPAD_TOP_PATH)

    build_common.tag_service('kaspad', commit_number)
    KT_logger.info('Finished building kaspad image(s).')


if __name__ == "__main__":
    build_and_tag_kaspad_image()
