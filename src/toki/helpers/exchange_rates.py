from datetime import datetime, time
from toki.dynamodb import dynamodb_client
from itertools import groupby


def extract_change_rates(start_date: datetime, end_date: datetime) -> dict:
    """

    :param datetime start_date:
    :param datetime end_date:
    :return:
    """
    response = dynamodb_client.scan(
        TableName="consumption_rates",
        FilterExpression="asDate BETWEEN :start_date AND :end_date",
        ExpressionAttributeValues={
            ":start_date": {"S": start_date.strftime('%Y-%m-%d')},
            ":end_date": {"S": end_date.strftime('%Y-%m-%d')},
        }
    )

    sorted_items = sorted(response['Items'], key=lambda x: x['asDate']['S'])
    grouped_items = groupby(sorted_items, key=lambda x: x['asDate']['S'])

    grouped_results = {}
    for key, group in grouped_items:
        rates = {item['asTime']['S']: item['rate']['N'] for item in group}
        grouped_results[key] = rates

    return grouped_results
