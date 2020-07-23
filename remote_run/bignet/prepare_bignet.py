from kaspy_tools.remote_run.bignet.aws.s3_tools import S3_Client

def main_preparation():
    s3_client = S3_Client()
    s3_client.get_S3_bucket()
    pass


if __name__ == '__main__':
    main_preparation()