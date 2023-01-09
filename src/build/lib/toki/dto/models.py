import faust
from abc import ABC
from dataclasses_avroschema import AvroModel, types
import decimal
import dataclasses
import datetime
from typing import List, Optional


@dataclasses.dataclass
class MeteringPointConsumptionEntityModel(faust.Record, AvroModel, ABC, serializer='avro_metering_point_consumption'):
    """
    The main Model DTO used to transfer CSV items across the different microservicess
    """
    metering_point_id: int
    timestamp: datetime.datetime
    kwh: decimal.Decimal = types.Decimal(precision=4, scale=2, default=decimal.Decimal(value=0))


@dataclasses.dataclass
class UserIdentity(AvroModel):
    principalId: str

    class Meta:
        namespace = "types.userIdentity_type"
        schema_doc = False


class RequestParameters(AvroModel):
    principalId: str
    region: str
    sourceIPAddress: str


class ResponseElements(AvroModel):
    contentLength: int = dataclasses.field(metadata={"aliases": ["content-length"]})
    xAmzRequestId: str = dataclasses.field(metadata={"aliases": ["x-amz-request-id"]})
    xMinioDeploymentId: str = dataclasses.field(metadata={"aliases": ["x-minio-deployment-id"]})
    xMinioOriginEndpoint: str = dataclasses.field(metadata={"aliases": ["x-minio-origin-endpoint"]})


class S3Bucket(AvroModel):
    name: str
    ownerIdentity: UserIdentity
    arn: str


class UserMetadata(AvroModel):
    contentType: str = dataclasses.field(metadata={"aliases": ["content-type"]})


class S3Object(AvroModel, ABC):
    key: str
    size: int
    eTag: str
    contentType: str
    userMetadata: UserMetadata
    sequencer: str


class S3Source(AvroModel):
    host: str
    port: str
    userAgent: str


class S3DataContainer(AvroModel):
    s3SchemaVersion: str
    configurationId: str
    bucket: S3Bucket
    object: S3Object


class BucketFileEntity(AvroModel):
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


@dataclasses.dataclass
class S3BucketFile(faust.Record, AvroModel, serializer='avro_new_csv_file_event'):
    EventName: str
    Key: str
    # Records: List[BucketFileEntity]
