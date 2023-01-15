import boto3
clientArgs = {
    'aws_access_key_id': 'admin',
    'aws_secret_access_key': 'Eemi8cah',
    'endpoint_url': 'http://localhost:20083',
}

minio_s3_client = boto3.client("s3", **clientArgs)
minio_s3_resource = boto3.resource("s3", **clientArgs)
