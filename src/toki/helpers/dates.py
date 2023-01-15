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
    for n in range(int((end_datetime - start_datetime).days + 1) * 24):
        yield start_datetime + timedelta(hours=n)


def datetime_month_start(value: datetime)-> datetime:
    """
    The method is  returning the datetime object of the beginning of the month of its current value

    :param datetime value:
    :return:
    """
    try:
        return value.replace(day=1, minute=0, second=0, hour=0, microsecond=0)
    except (AttributeError, ValueError) as ex:
        raise ex
