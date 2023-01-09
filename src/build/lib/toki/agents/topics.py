from toki.app import app
from toki.dto.models import S3BucketFile

new_files_topic = app.topic('toki-csv-files', partitions=1, key_type=str, value_type=S3BucketFile)
