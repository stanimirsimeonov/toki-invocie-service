from toki.dynamodb import dynamod_resource
import logging
from toki.app import app, settings
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def create_table(params: dict):
    """

    :param params:
    :return:
    """
    try:
        table = dynamod_resource.create_table(**params)
        table.wait_until_exists()
        return table
    except ClientError as ex:
        # must be decided what to be happened here. Using Happy path!
        return False
