import datetime
from toki.dto.models_new_csv_files import S3BucketFile
from toki.app import app, logger
from toki.topics import new_files_topic
from toki.helpers.event_filters import filter_event_valid_moved_files
from toki.helpers.exchange_rates import extract_change_rates
from toki.helpers.files import open_csv_as_dataframe, IOString_to_s3
from toki.helpers.dates import datetime_month_start
from decimal import Decimal
from toki.minio import minio_s3_client
import pandas as pd
import io
from typing import List


@app.agent(new_files_topic)
async def on_valid_file(csv_files):
    """
    An Agent which validate every single csv file

    :param csv_files:
    :return:
    """
    async for event in csv_files.filter(filter_event_valid_moved_files):
        a: List[S3BucketFile] = event
        for s3_batch_files in event.Records:
            bucket = s3_batch_files.s3.bucket.name
            object_name = s3_batch_files.s3.object.key

            initial_df = open_csv_as_dataframe(
                bucket=bucket,
                objectName=object_name,
                columns=["metering_point_id", "timestamp", "kwh"]
            )
            # we have to find out the min date of entire the csv file and max date.
            # we must find them to make sure we are capable to extract the price rates and multiply the usage after that

            # convert timestamp to datetime in a buffering column (later will be exported as human-readable)
            initial_df['date_time'] = pd.to_datetime(initial_df['timestamp'], unit='ms')

            start_date_from = datetime_month_start(initial_df["date_time"].min())
            end_date_to = initial_df["date_time"].max()

            exchange_rates = extract_change_rates(start_date=start_date_from, end_date=end_date_to)

            # generating two more series as helpers in further operations
            initial_df['date'] = initial_df['date_time'].dt.strftime('%Y-%m-%d')
            initial_df['time'] = initial_df['date_time'].dt.strftime('%H:%M:%S')

            # let's iterate over the Dataframe and add amount and prive for every row
            for index, row in initial_df.iterrows():
                price_rate = Decimal(exchange_rates[row['date']][row['time']])

                initial_df.at[index, 'price'] = price_rate
                initial_df.at[index, 'amount'] = Decimal(row["kwh"]) * price_rate

            split_by_metering = initial_df.groupby('metering_point_id')

            for metering_id, meter in split_by_metering:
                # convert the dataframe to a CSV string
                csv_buffer = io.StringIO()
                meter.to_csv(csv_buffer)
                IOString_to_s3(
                    csv_buffer,
                    bucket='pre-invoice-raw-files',
                    objectName="{year}/{month}/{metering_id}.csv".format(
                        year=datetime.datetime.now().year,
                        month=datetime.datetime.now().month,
                        metering_id=metering_id
                    ))
