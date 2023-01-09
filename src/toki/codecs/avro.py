from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers.faust import FaustSerializer
from simple_settings import settings
import json
from toki.dto.models import   S3BucketFile

# Initialize Schema Registry Client
client = SchemaRegistryClient(url=settings.SCHEMA_REGISTRY_URL)


# Initialize Schema serializer for upcoming events according to the new files or existing files and their manipulation
avro_new_csv_file_event_serializer = FaustSerializer(
    client,
    "new_csv_file_event",
    S3BucketFile.avro_schema()
)

def avro_new_csv_file_event_codec():
    return avro_new_csv_file_event_serializer