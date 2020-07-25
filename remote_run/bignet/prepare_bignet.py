from kaspy_tools import kaspy_tools_constants
from kaspy_tools.remote_run.bignet.aws.s3_tools import S3_Client
from kaspy_tools.remote_run.bignet.aws.ECR_tools import ECR_Client
from kaspy_tools.local_run.kaspad_docker import build_kaspad
from kaspy_tools.local_run.kasparov_docker import build_kasparov


def main_preparation():
    verify_S3_bucket()
    create_all_kaspanet_images()
    push_all_images_to_aws_ECR()
    pass

def verify_S3_bucket():
    s3_client = S3_Client( aws_access_key_id=kaspy_tools_constants.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=kaspy_tools_constants.AWS_SECRET_ACCESS_KEY)
    s3_client.get_S3_bucket()

def create_all_kaspanet_images():
    build_kaspad.build_and_tag_kaspad_image()
    build_kasparov.build_and_tag_kasparov_services()
    build_kasparov.pull_postgres_image()

def push_all_images_to_aws_ECR():
    images_names = ['kaspad', 'kasparov-sync', 'kasparovd', 'postgres', ]
    rep_base='bignet'
    ecr_client = ECR_Client(aws_access_key_id=kaspy_tools_constants.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=kaspy_tools_constants.AWS_SECRET_ACCESS_KEY)
    for image_name in images_names:
        registry_id, repository_uri = ecr_client.get_repository(rep_name=f'{rep_base}/{image_name}')
        ecr_client.tag_images(rep_base='bignet',repository_uri=repository_uri, image_names=['kaspad'])
        ecr_client.push_an_image_to_ecr(repository_uri, image_name, 'latest')


if __name__ == '__main__':
    main_preparation()