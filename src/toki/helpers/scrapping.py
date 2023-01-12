from toki.app import app, settings, logger
from datetime import datetime, timedelta, date
from toki.common.http import fetch_all
import asyncio
from toki.helpers.dates import daterange


def build_exchange_rate_urls(scrape_date_from: datetime = None):
    """

    :param scrape_date_from:
    :return:
    """
    current_date_object = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if scrape_date_from is None:
        # if there is no set a date where we want to scrape from, we are using always yesterday.
        # Otherwise, we are scrapping UP to Yesterday
        scrape_date_from = current_date_object - timedelta(days=1)

    scrapping_date_to = current_date_object - timedelta(days=1)

    return [
        "https://us-central1-toki-take-home.cloudfunctions.net/prices/{}".format(d)
        for d in daterange(scrape_date_from.date(), scrapping_date_to.date())
    ]
