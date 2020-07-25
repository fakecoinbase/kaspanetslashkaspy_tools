import subprocess
import boto3
import base64
from kaspy_tools import kaspy_tools_constants
from kaspy_tools.logs import config_logger

KT_logger = config_logger.get_kaspy_tools_logger()

AWS_REGION = 'eu-central-1'
BIGNET_REP_NAME = 'bignet-rep'

class ECR_Client:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.ECR_client = boto3.client('ecr', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)


    def __login_to_ecr(self):
        authorization_response = self.ECR_client.get_authorization_token()

        authorization_base64 = authorization_response['authorizationData'][0]['authorizationToken']
        authorization_utf8 = base64.b64decode(authorization_base64).decode('UTF-8')
        username, password = authorization_utf8.split(":")

        authorization_url = authorization_response['authorizationData'][0]['proxyEndpoint']

        login_result = subprocess.run(f'docker login -u {username} -p {password} {authorization_url}', shell=True)
        assert login_result.returncode == 0, 'Failed to login to ECR.'

        KT_logger.debug('Logged in to ECR.')


    def get_all_repositories(self):
        response = self.ECR_client.describe_repositories(maxResults=1000)
        repositories = response['repositories']
        rep_names = [rep['repositoryName'] for rep in repositories]
        return rep_names

    def get_repository(self, *, rep_name):
        if rep_name in self.get_all_repositories():
            response = self.ECR_client.describe_repositories(repositoryNames=[rep_name])
            return response['repositories'][0]['registryId'], response['repositories'][0]['repositoryUri']
        response = self.ECR_client.create_repository(
            repositoryName=rep_name,
            imageTagMutability= 'IMMUTABLE',
            imageScanningConfiguration={
                'scanOnPush':  False
            }
        )
        return response['repository']['registryId'], response['repository']['repositoryUri']

    def push_an_image_to_ecr(self, repository_uri, image_name, image_tag):
        self.__login_to_ecr()
        push_result = subprocess.run(f'docker push {repository_uri}:{image_tag}', shell=True, capture_output=True)
        push_result.check_returncode()

    @staticmethod
    def tag_images(*, rep_base='bignet', repository_uri='', image_names=None):
        for iname in image_names:
            cmd_args = []
            cmd_args.extend(['docker', 'tag', f'{iname}:latest', f'{repository_uri}:latest'])
            completed_process = subprocess.run(args=cmd_args, capture_output=True)
            completed_process.check_returncode()



if __name__ == '__main__':
    my_ecr = ECR_Client(aws_access_key_id=kaspy_tools_constants.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=kaspy_tools_constants.AWS_SECRET_ACCESS_KEY)
    names = my_ecr.get_all_repositories()
