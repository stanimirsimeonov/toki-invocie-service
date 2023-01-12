from toki.app import app, logger
from toki.topics import validation_files_topic
from toki.minio import minio_s3_resource
import datetime
from botocore.exceptions import ClientError
from toki.postprocessors.sink_save_new_file_data_to_dynamodb import write_file_information_to_db


@app.agent(validation_files_topic, sink=[write_file_information_to_db])
async def on_validation_uploaded_file(csv_files):
    """
    The agent is caring when some file went through the validation process will got a status. We have to decide what to
    do with the given file.

    Tasks:
        1. In our case we want to move all the valid files to different bucket than invalid files.
        2. We have to store in a db what file is being uploaded
            2.1 We have to write the errors.
            2.1 We have to write the status of the file

    :param List[S3CSValidatedFile] csv_files:
    :return:
    """
    async for event in csv_files:

        new_file_name = "{timestamp}_{bucket}_{file}".format(
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            bucket=event.bucket,
            file=event.file
        )
        # decider which bucket to be moved files to
        new_bucket = 'mistaken-files' if event.errors.__len__() > 0 else 'valid-files'

        try:
            # Minio have no move operation out of the box and we have to think out of the box. That's why we are copying
            # and after that deleting the older file. which give us the same value
            minio_s3_resource.Object(new_bucket, new_file_name).copy_from(
                # where we are copy data from
                CopySource='{bucket}/{file}'.format(bucket=event.bucket, file=event.file)
            )
            minio_s3_resource.Object('new-files', event.file).delete()
            logger.info(f"[on_validation_uploaded_file]: The file moved")

        except ClientError as ex:
            logger.error(f"[on_validation_uploaded_file]: The file can't be copied: {ex.response}")
            logger.exception(ex)
            raise ex
        finally:
            yield event
