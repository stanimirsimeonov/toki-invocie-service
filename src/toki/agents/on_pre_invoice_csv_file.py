import datetime
from toki.dto.models_new_csv_files import S3BucketFile
from toki.app import app, logger
from toki.topics import new_files_topic
from toki.helpers.event_filters import filter_event_valid_files_for_invoices
from decimal import Decimal

import urllib.parse
from toki.helpers.exchange_rates import extract_change_rates
from toki.helpers.files import open_csv_as_dataframe, IOString_to_s3
from toki.helpers.dates import datetime_month_start
from decimal import Decimal
from toki.minio import minio_s3_client
import pandas as pd
from io import BytesIO
import simplejson as json

import io
from typing import List


@app.agent(new_files_topic)
async def on_pre_invoice_file(csv_files):
    """
    An Agent which validate every single csv file

    :param csv_files:
    :return:
    """
    async for event in csv_files.filter(filter_event_valid_files_for_invoices):
        for s3_batch_files in event.Records:
            bucket = s3_batch_files.s3.bucket.name
            object_name = urllib.parse.unquote(s3_batch_files.s3.object.key)
            initial_df = open_csv_as_dataframe(
                bucket=bucket,
                objectName=object_name,
                columns=[
                    "metering_point_id",
                    "timestamp",
                    "kwh",
                    "date_time",
                    "date",
                    "time",
                    "price",
                    "amount",
                ]
            )
            initial_df['timestamp'] = pd.to_datetime(initial_df['timestamp'], unit='ms')
            initial_df['date'] = initial_df['timestamp'].dt.date
            # to make sure we are able to aggregate by the field because otherwise it will throw an error because ot string type
            initial_df['amount'] = initial_df['amount'].apply(lambda x: Decimal(x))
            initial_df['metering_point_id'] = initial_df['metering_point_id']

            # group the dataframe by date and sum the amount column
            df_grouped = initial_df.groupby('date').agg({'amount': ['sum', 'mean']})
            df_grouped.columns = ['total_amount', 'average_amount']
            df_grouped['date'] = df_grouped.index
            df_grouped.reset_index(drop=True, inplace=True)

            # create file-like object
            json_data = io.BytesIO()

            # Serialize dataframe to json and write to file-like object
            df_grouped['date'] = df_grouped['date'].apply(lambda x: x.strftime("%Y-%m-%d"))
            data = df_grouped.to_json(orient='records')
            formated_json = json.dumps(json.loads(data), indent=4)
            json_data.write(formated_json.encode())

            # seek to start of file-like object
            json_data.seek(0)

            # upload the json file to s3 bucket
            minio_s3_client.put_object(
                Body=json_data.getvalue(),
                Bucket='invoices',
                Key="{year}/{month}/{metering_id}.json".format(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    metering_id=initial_df.iloc[0]['metering_point_id']
                )
            )

            # we have to sum the rows per day
            pass
