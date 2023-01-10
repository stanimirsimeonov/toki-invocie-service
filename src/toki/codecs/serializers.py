from schema_registry.serializers.faust import FaustSerializer
from toki.dto.models_new_csv_files import S3BucketFile
from toki.dto.models_corrupted_files import S3CSVInvalidFile
from toki.dto.models_valid_files import S3CSValidFile

from toki.schema_registry import client

# Initialize Schema serializer for upcoming events according to the new files or existing files and their manipulation
avro_new_csv_file_event_serializer = FaustSerializer(
    client,
    "new_csv_file_event",
    S3BucketFile.avro_schema()
)

avro_mistaken_files_serializer = FaustSerializer(
    client,
    "mistaken_files_event",
    S3CSVInvalidFile.avro_schema()
)

avro_valid_files_serializer = FaustSerializer(
    client,
    "valid_files_event",
    S3CSValidFile.avro_schema()
)
