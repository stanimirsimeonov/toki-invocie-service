from toki.app import app, settings, logger
from datetime import datetime, timedelta, date
from toki.common.http import fetch_all
import asyncio
from toki.helpers.dates import daterange, timerange
from toki.dynamodb import dynamod_resource
import re
from decimal import Decimal
import json



def extract_exchange_rates(scrape_date_from: datetime = None):
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


@app.crontab('* * * * *')
async def every_day_at_8_pm():
    """
    The crontab must be executed once per day  to execute or catchup with all the rates
    :return:
    """

    scraping_links = extract_exchange_rates()
    result = await fetch_all(scraping_links)

    date_regex = re.compile(r'(\d{4}\-\d{2}\-\d{2})')

    for rate_per_day in result:

        date_string = date_regex.search(rate_per_day.get('url')).group(0)
        date_object_from = datetime.strptime(date_string, '%Y-%m-%d')
        rate_items = rate_per_day.get('items')

        records = [
            {
                # "timestamp": datetime.strftime(key, '%Y-%m-%d %H:%M:%S'),
                "timestamp":  datetime.timestamp(key),
                "time": datetime.strftime(key, '%H:%M:%S'),
                "date": datetime.strftime(key, '%Y-%m-%d'),
                "rate": value
            }
            for i, (key, value) in enumerate(
                zip(
                    timerange(date_object_from, date_object_from + timedelta(hours=23, minutes=59, seconds=59)),
                    rate_items
                )
            )
        ]

        table = dynamod_resource.Table(settings.VAR_DYNAMODB_TABLE_CONSUMPTION_RATES.get('TableName'))
        try:
            with table.batch_writer() as batch:
                for record in records:
                    batch.put_item(Item=json.loads(json.dumps(record), parse_float=Decimal))

        except Exception as err:
            logger.error(err)
