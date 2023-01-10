from toki.codecs.serializers import (
    avro_mistaken_files_serializer,
    avro_valid_files_serializer,
    avro_new_csv_file_event_serializer
)


def avro_new_csv_file_event_codec():
    """
    The main avro codec used to translate to DTO the events coming from the MINIO
    :return FaustSerializer:
    """
    return avro_new_csv_file_event_serializer


def avro_valid_files_event_codec():
    """
    The main avro codec used to translate to DTO for transferred events regarding the valid files after their validation

    :return FaustSerializer:
    """
    return avro_valid_files_serializer


def avro_mistaken_files_event_codec():
    """
    The main avro codec used to translate to DTO for transferred events regarding the invalid files after
    their validation

    :return FaustSerializer:
    """
    return avro_mistaken_files_serializer
