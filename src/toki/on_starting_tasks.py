from toki.dynamodb import dynamod_resource
import logging
from toki.app import app
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


@app.task
async def on_started_ensure_created_table():
    try:
        params = {
            'TableName': 'uploaded_files',
            'KeySchema': [
                {'AttributeName': 'bucket', 'KeyType': 'HASH'},
                {'AttributeName': 'filename', 'KeyType': 'RANGE'},
            ],
            'LocalSecondaryIndexes': [
                {
                    'IndexName': "IndexCreatingRange",
                    'KeySchema': [
                        {'AttributeName': 'bucket', 'KeyType': 'HASH'},
                        {'AttributeName': 'created_at', 'KeyType': 'RANGE'},
                    ],
                    'Projection': {
                        'ProjectionType': "ALL"
                    }
                }
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'bucket', 'AttributeType': 'S'},
                {'AttributeName': 'filename', 'AttributeType': 'S'},
                {'AttributeName': 'created_at', 'AttributeType': 'S'},
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 100,
                'WriteCapacityUnits': 100
            }
        }

        table = dynamod_resource.create_table(**params)
        logging.info(f"The table \"uploaded_files\" is missing. \n Created... \nReady. Continuing ....")
        table.wait_until_exists()
        return table
    except ClientError as ex:
        logging.error(f"The table \"uploaded_files\" cannot be created: {ex.response['Error']}")
        # logger.exception(ex)
        return False
