from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspa_model import kaspa_address
from kaspy_tools.local_run import build_common

kaspad_branch = 'v0.5.0-dev'


def build_and_tag_kaspad_image():
    """
    Generates a build to be used by the setUpClass() method of the test-kits.
    """
    commit_number = build_common.get_git_commit(kaspy_tools_constants.KASPAD_TOP_PATH, branch=kaspad_branch)
    build_dir = kaspy_tools_constants.LOCAL_RUN_PATH + '/kaspad_docker'
    build_common.build_image(service_name='kaspad', build_dir=build_dir, commit_number=commit_number,
                             context_dir=kaspy_tools_constants.KASPAD_TOP_PATH)

    build_common.tag_service('kaspad', commit_number)


if __name__ == "__main__":
    build_and_tag_kaspad_image()