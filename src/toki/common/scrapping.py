from faust.cli import option
from toki.app import app, settings, logger
from datetime import datetime, timedelta
from toki.common.http import fetch_all
from toki.helpers.dates import timerange
from toki.dynamodb import dynamod_resource
import re
from decimal import Decimal
import json
from toki.helpers.scrapping import build_exchange_rate_urls


async def scrape_exchange_rates(from_date: str):
    """
    A method which is responsible to download all the price rates for the given period from starting point which
    comes as argument

    :param str from_date:
    :return:
    """
    datetime_object = datetime.strptime(from_date, '%Y-%m-%d')
    scraping_links = build_exchange_rate_urls(datetime_object)
    result = await fetch_all(scraping_links)

    date_regex = re.compile(r'(\d{4}\-\d{2}\-\d{2})')

    for rate_per_day in result:

        date_string = date_regex.search(rate_per_day.get('url')).group(0)
        date_object_from = datetime.strptime(date_string, '%Y-%m-%d')
        rate_items = rate_per_day.get('items')

        records = [
            {
                "asTimestamp": datetime.timestamp(key),
                "asTime": datetime.strftime(key, '%H:%M:%S'),
                "asDate": datetime.strftime(key, '%Y-%m-%d'),
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
            # what to be done as custom exception
            logger.error(err)
            return False
