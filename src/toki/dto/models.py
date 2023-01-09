import faust
from abc import ABC
from dataclasses_avroschema import AvroModel, types
import decimal
import dataclasses
import datetime
from typing import List, Optional


@dataclasses.dataclass
class UserIdentity(faust.Record, AvroModel, ABC):
    principalId: str

    class Meta:
        namespace = "types.userIdentity_type"
        schema_doc = False


@dataclasses.dataclass
class RequestParameters(faust.Record, AvroModel, ABC):
    principalId: str
    region: str
    sourceIPAddress: str


@dataclasses.dataclass
class ResponseElements(faust.Record, AvroModel, ABC):
    contentLength: int = dataclasses.field(metadata={"aliases": ["content-length"]})
    xAmzRequestId: str = dataclasses.field(metadata={"aliases": ["x-amz-request-id"]})
    xMinioDeploymentId: str = dataclasses.field(metadata={"aliases": ["x-minio-deployment-id"]})
    xMinioOriginEndpoint: str = dataclasses.field(metadata={"aliases": ["x-minio-origin-endpoint"]})


@dataclasses.dataclass
class S3Bucket(faust.Record, AvroModel, ABC):
    name: str
    ownerIdentity: UserIdentity
    arn: str


@dataclasses.dataclass
class UserMetadata(faust.Record, AvroModel, ABC):
    contentType: str = dataclasses.field(metadata={"aliases": ["content-type"]})


@dataclasses.dataclass
class S3Object(faust.Record, AvroModel, ABC):
    key: str
    size: int
    eTag: str
    contentType: str
    userMetadata: UserMetadata
    sequencer: str


@dataclasses.dataclass
class S3Source(faust.Record, AvroModel, ABC):
    host: str
    port: str
    userAgent: str


@dataclasses.dataclass
class S3DataContainer(faust.Record, AvroModel, ABC):
    s3SchemaVersion: str
    configurationId: str
    bucket: S3Bucket
    object: S3Object


@dataclasses.dataclass
class BucketFileEntity(faust.Record, AvroModel, ABC):
    eventVersion: str
    eventSource: str
    awsRegion: str
    eventTime: str
    eventName: str

    userIdentity: UserIdentity
    requestParameters: RequestParameters
    responseElements: ResponseElements
    s3: S3DataContainer
    source: S3Source


class S3BucketFile(faust.Record, AvroModel, ABC, serializer='avro_new_csv_file_event'):
    EventName: str
    Key: str
    Records: List[BucketFileEntity]


@dataclasses.dataclass
class MeteringPointConsumptionEntityModel(faust.Record, AvroModel, ABC, serializer='avro_metering_point_consumption'):
    """
    The main Model DTO used to transfer CSV items across the different microservicess
    """
    metering_point_id: int
    timestamp: datetime.datetime
    kwh: decimal.Decimal = types.Decimal(precision=4, scale=2, default=decimal.Decimal(value=0))
