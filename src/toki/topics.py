from toki.app import app
from toki.dto.models import S3BucketFile
from toki.codecs.avro import avro_new_csv_file_event_serializer
new_files_topic = app.topic('toki-csv-files', partitions=1, value_serializer='json', value_type=S3BucketFile)