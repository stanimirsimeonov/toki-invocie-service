import faust
from abc import ABC
from dataclasses_avroschema import AvroModel
import dataclasses
from typing import List


@dataclasses.dataclass
class S3CSVErrorItem(faust.Record, AvroModel, ABC):
    """
    The DTO which represent how the CSV error looks like
    """
    column: str
    message: str
    row: int
    value: str


@dataclasses.dataclass
class S3CSValidatedFile(faust.Record, AvroModel, ABC, serializer='avro_validated_event'):
    """
    The DTO which represent how the transferred object for mistaken file looks like
    """
    bucket: str
    file: str
    errors: List[S3CSVErrorItem]
