from toki.app import app
from datetime import datetime, timedelta
from toki.common.scrapping import scrape_exchange_rates


@app.crontab('0 1 * * *')
async def every_day_at_00_01_am():
    """
    The crontab must be executed once per day  to execute or catchup with all the rates

    :return:
    """
    await scrape_exchange_rates(
        (datetime.now().replace(hour=0, microsecond=0, minute=0, second=0) - timedelta(days=1)).strftime('%Y-%m-%d')
    )
