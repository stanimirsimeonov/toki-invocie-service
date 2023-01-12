from datetime import timedelta, date, datetime
import math

def daterange(start_date: date, end_date: date):
    """
    Create a change to loop over a range of dates and make list of dates between start and end dates

    :param date start_date:
    :param date end_date:
    :return:
    """
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def timerange(start_datetime: date, end_datetime: date):
    """
    Create a change to loop over a range of datetime and make list of hours between start and end datetimes

    :param date start_datetime:
    :param date end_datetime:
    :return:
    """
    for n in range(int((end_datetime - start_datetime).days  + 1) * 24):
        yield start_datetime + timedelta(hours=n)
