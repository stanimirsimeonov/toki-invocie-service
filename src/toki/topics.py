from toki.app import app
from toki.dto.models_new_csv_files import S3BucketFile
from toki.dto.models_validated_files import S3CSValidatedFile

new_files_topic = app.topic(
    'toki-csv-files',
    partitions=1,
    value_serializer='json',
    value_type=S3BucketFile
)

validation_files_topic = app.topic(
    'toki-validation-files',
    partitions=8,
    acks=True,
    value_serializer='json',
    value_type=S3CSValidatedFile
)



