import datetime
from toki.dynamodb import dynamod_resource
from toki.dto.models_validated_files import S3CSValidatedFile
from toki.app import settings


async def write_file_information_to_db(value: S3CSValidatedFile):
    """
    A callback hook invoked by the faust.Agent as a sink to inform the database

    :param S3CSVInvalidFile value:
    :return :
    """
    table = dynamod_resource.Table(settings.VAR_DYNAMODB_TABLE_UPLOADED_FILES.get('TableName'))
    table.put_item(Item={
        'bucket': value.bucket,
        'filename': value.file,
        'status': 'invalid' if len(value.errors) > 0 else 'valid',
        'errors': [error.dumps() for error in value.errors],
        'created_at': str(datetime.datetime.now()),
        'updated_at': None
    })
    return value
