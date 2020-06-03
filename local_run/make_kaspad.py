from kaspy_tools import kaspy_tools_constants
from kaspy_tools.kaspa_model import kaspa_address
from kaspy_tools.local_run import run_dev

def make_kaspad_docker_image():
    """
    Generates a build to be used by the setUpClass() method of the test-kits.
    :param mining_address: kaspanet address to be used when editing docekr-compose file.
    """

    mining_address = kaspa_address.KaspaAddress()
    run_dev.remove_all_images_and_containers()
    run_dev.create_docker_compose_file(mining_address)

    # The following function call is synchronuous one, so once the function returns, the image was built.
    run_dev.docker_image_build('kaspad', kaspy_tools_constants.KASPAD_TOP_PATH)
    run_dev.tag_image_latest('kaspad')

if __name__ == "__main__":
    make_kaspad_docker_image()
