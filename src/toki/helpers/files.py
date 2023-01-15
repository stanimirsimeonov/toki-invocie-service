import io

from toki.minio import minio_s3_client, minio_s3_resource
import pandas as pd
from typing import List
from botocore.exceptions import ClientError


def open_csv_as_dataframe(bucket: str, objectName: str, columns: List[str]):
    """
    Open a csv file from a bucket and return it as pandas Dataframe.

    :param string bucket:
    :param string objectName:
    :param List[str] columns:
    :return :
    """
    try:
        obj = minio_s3_client.get_object(Bucket=bucket, Key=objectName)
        return pd.read_csv(
            obj['Body'],
            header=0,
            dtype="string",
            names=columns
        )
    except ClientError as ex:
        # might be done with custom exception
        raise ex


def IOString_to_s3(stream: io.StringIO, bucket: str, objectName: str):
    """
    Wrapper which stores Streams to the S3 we are using

    :param stream:
    :param bucket:
    :param objectName:
    :return:
    """
    try:
        return minio_s3_client.put_object(
            Bucket=bucket,
            Key=objectName,
            Body=stream.getvalue()
        )
    except ClientError as ex:
        # might be done with custom exception
        raise ex
