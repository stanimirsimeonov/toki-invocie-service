from toki.app import app
from toki.dto.models_new_csv_files import S3BucketFile
from toki.dto.models_corrupted_files import S3CSVInvalidFile
from toki.dto.models_valid_files import S3CSValidFile

new_files_topic = app.topic(
    'toki-csv-files',
    partitions=1,
    value_serializer='json',
    value_type=S3BucketFile
)

error_files_topic = app.topic(
    'toki-corrupted-files',
    partitions=1,
    value_serializer='json',
    value_type=S3CSVInvalidFile
)

valid_files_topic = app.topic(
    'toki-valid-files',
    partitions=1,
    value_serializer='json',
    value_type=S3CSValidFile
)
