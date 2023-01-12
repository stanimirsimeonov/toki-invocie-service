import boto3
from botocore.exceptions import ClientError

# import urllib3
# urllib3.disable_warnings()



clientArgs = {
    'aws_access_key_id': 'a',
    'aws_secret_access_key': 'a',
    'endpoint_url': 'http://localhost:28000',
    'region_name': 'us-east-1'

}

dynamodb_client = boto3.client("dynamodb", **clientArgs)
dynamod_resource = boto3.resource("dynamodb", **clientArgs)



