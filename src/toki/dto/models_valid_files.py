import faust
from abc import ABC
from dataclasses_avroschema import AvroModel
import dataclasses


@dataclasses.dataclass
class S3CSValidFile(faust.Record, AvroModel, ABC, serializer='avro_valid_files_event'):
    """
    The DTO which represent how the transferred object for valid file looks like
    """
    bucket: str
    file: str
