import os
import json
import re
import boto3
from kaspy_tools import kaspy_tools_constants

AWS_ENVIRONMENT_NAME = os.getenv('AWS_ENVIRONMENT_NAME', 'dev')
AWS_REGION = 'eu-central-1'
BUCKET_NAME = 'bignet-' + AWS_REGION

class S3_Client:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def upload_file(self, body, s3_path):
        s3 = boto3.resource('s3')
        s3_version_file = s3.Object(BUCKET_NAME, s3_path)
        s3_version_file.put(Body=body)

    def upload_files(self, directory, s3_root):
        self.get_S3_bucket()

        s3 = boto3.resource('s3')
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                s3_path = os.path.join(s3_root, re.sub(f'^{directory}\/?', '', subdir, 1), file)
                s3.meta.client.upload_file(local_path, BUCKET_NAME, s3_path)
                print(f'File {local_path} uploaded to {s3_path}.')

    def get_S3_bucket(self, bucket_name=BUCKET_NAME):
        bucket_names = [bucket['Name'] for bucket in self.get_all_our_buckets()[0]]
        if bucket_name in bucket_names:
            return

        # print(f'Bucket {BUCKET_NAME} not found. Creating...')
        self.s3_client.create_bucket(
            ACL='private',
            CreateBucketConfiguration={'LocationConstraint': AWS_REGION},
            Bucket=bucket_name
        )

        print(f'Bucket {BUCKET_NAME} successfully created.')

    def get_all_our_buckets(self):
        ans = self.s3_client.list_buckets()
        bucket_list = ans['Buckets']
        bucket_owner = ans['Owner']
        return bucket_list, bucket_owner


if __name__ == '__main__':
    my_s3 = S3_Client()
    my_s3.get_all_our_buckets()
    pass