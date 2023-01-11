import datetime

from toki.app import app
from toki.topics import error_files_topic
from toki.minio import minio_s3_resource


@app.agent(error_files_topic)
async def on_validation_valid_csv_file_agent(csv_files):
    async for event in csv_files:
        minio_s3_resource.Object(
            'mistaken-files', "{timestamp}_{bucket}_{file}".format(
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                bucket=event.bucket,
                file=event.file
            )
        ).copy_from(
            CopySource='{bucket}/{file}'.format(bucket=event.bucket, file=event.file)
        )
        minio_s3_resource.Object('new-files', event.file).delete()
        yield event
