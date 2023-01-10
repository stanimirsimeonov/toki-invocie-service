import pandas as pd


def pandas_is_valid_timestamp(series: pd.Series) -> bool:
    """
    Custom handler for the validation of CSV file based on the pandas_schema

    :param pd.Series series:
    :return bool:
    """
    try:
        return series.str.len() == 13
    except Exception as ex:
        return False
