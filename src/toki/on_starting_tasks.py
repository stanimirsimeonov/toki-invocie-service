from toki.dynamodb import dynamod_resource
import logging
from toki.app import app, settings
from botocore.exceptions import ClientError
from toki.helpers.dynamodb import create_table

logger = logging.getLogger(__name__)


@app.task
async def on_started_ensure_dynamodb_tables():
    """
    Migrator:
    Creates all the tables in dynamoDB if they are not presenting

    :return:
    """
    logger.info(f"[DynamoDB] ensure table: {settings.VAR_DYNAMODB_TABLE_UPLOADED_FILES.get('TableName')}")
    create_table(settings.VAR_DYNAMODB_TABLE_UPLOADED_FILES)

    logger.info(f"[DynamoDB] ensure table: {settings.VAR_DYNAMODB_TABLE_CONSUMPTION_RATES.get('TableName')}")
    create_table(settings.VAR_DYNAMODB_TABLE_CONSUMPTION_RATES)