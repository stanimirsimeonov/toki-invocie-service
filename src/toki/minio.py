import boto3
from botocore.exceptions import ClientError

# import urllib3
# urllib3.disable_warnings()

clientArgs = {
    'aws_access_key_id': 'admin',
    'aws_secret_access_key': 'Eemi8cah',
    'endpoint_url': 'http://localhost:20083',
}

minio = boto3.client("s3", **clientArgs)
