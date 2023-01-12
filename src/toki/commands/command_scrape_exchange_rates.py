from faust.cli import option
from toki.app import app
from toki.common.scrapping import scrape_exchange_rates

@app.command(
    option(
        '--from-date',
        type=str,
        default=None,
        help='What date (YYYY-mm-ss) to be used as initial date to scrape data from?'
    ),
)
async def scrape_exchanges(self, from_date: str):
    """
    Scrape rates for a particular

    :param self:
    :param from_date:
    :return:
    """
    await scrape_exchange_rates(from_date=from_date)
