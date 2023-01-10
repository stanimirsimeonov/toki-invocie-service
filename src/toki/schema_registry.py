from schema_registry.client import SchemaRegistryClient

from simple_settings import settings

# Initialize Schema Registry Client
client = SchemaRegistryClient(url=settings.SCHEMA_REGISTRY_URL)
