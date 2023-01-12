from schema_registry.serializers.faust import FaustSerializer
from toki.dto.models_new_csv_files import S3BucketFile
from toki.dto.models_validated_files import S3CSValidatedFile

from toki.schema_registry import client

# Initialize Schema serializer for upcoming events according to the new files or existing files and their manipulation
avro_new_csv_file_event_serializer = FaustSerializer(
    client,
    "new_csv_file_event",
    S3BucketFile.avro_schema()
)

avro_validated_serializer = FaustSerializer(
    client,
    "validation_csv_event",
    S3CSValidatedFile.avro_schema()
)

