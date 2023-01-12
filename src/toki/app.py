import faust
import logging
from simple_settings import settings
from logging.config import dictConfig
from toki.dynamodb import dynamod_resource

logger = logging.getLogger(__name__)

app = faust.App(
    version=1,
    autodiscover=True,
    origin='toki',
    broker_max_poll_records=1,
    id="1",
    broker=settings.KAFKA_BOOTSTRAP_SERVER,
    logging_config=dictConfig(settings.LOGGING),
)


def main() -> None:
    app.main()


