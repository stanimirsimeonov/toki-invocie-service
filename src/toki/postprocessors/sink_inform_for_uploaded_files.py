from typing import List
from toki.topics import validation_files_topic
from toki.dto.models_validated_files import S3CSValidatedFile


async def inform_for_validated_status_of_file(value: List[S3CSValidatedFile]):
    """
    The given callback is invoked immediately after the file is being processed. As Value are passed all the uploaded
    files into minio and their path as bucket/file and errors if there are

    :param List value:
    :return:
    """

    for file in value:
        send_topic_key = "{bucket}_{file}".format(**file)
        await validation_files_topic.send(key=send_topic_key, value_serializer="json", value=file)
