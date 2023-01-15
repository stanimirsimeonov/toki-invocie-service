from toki.serialization_codecs.serializers import (
    avro_new_csv_file_event_serializer,
    avro_validated_serializer
)


def avro_new_csv_file_event_codec():
    """
    The main avro codec used to translate to DTO the events coming from the MINIO
    :return FaustSerializer:
    """
    return avro_new_csv_file_event_serializer


def avro_validated_event_codec():
    """
    The main avro codec used to translate to DTO for transferred events regarding the valid files after their validation

    :return FaustSerializer:
    """
    return avro_validated_serializer

