from toki.app import app
from toki.topics import new_files_topic
import pandas as pd
from toki.minio import minio
from toki.postprocessors.sink_inform_for_uploaded_files import inform_for_validated_status_of_file
from toki.validation.csv_schemas import incoming_csv_validation_schema


@app.agent(new_files_topic, sink=[inform_for_validated_status_of_file])
async def greet(csv_files):
    async for event in csv_files.filter(lambda x: x.EventName == 's3:ObjectCreated:Put'):

        # extract all the files which have arrived; # there is a chance to split the agent into two, to reduce the
        # responsibility of the given agent. Then we can just process the files and send for another agent to valid them
        # for the task we will combine the tasks because they are too small and to reduce the time for sipping

        files = [
            {
                "bucket": bucket_file_entity.s3.bucket.name,
                "file": bucket_file_entity.s3.object.key
            }
            for bucket_file_entity in event.Records
        ]

        for file in files:
            obj = minio.get_object(Bucket=file.get("bucket"), Key=file.get("file"))
            initial_df = pd.read_csv(obj['Body'], header=0, dtype="string")
            errors = incoming_csv_validation_schema.validate(initial_df)

            # escape from the pandas dataclass in order to convert it into fuast.Record
            file['errors'] = [
                {
                    "column": error.column,
                    "message": error.message,
                    "row": error.row,
                    "value": error.value
                }
                for error in errors
            ]
        yield files
