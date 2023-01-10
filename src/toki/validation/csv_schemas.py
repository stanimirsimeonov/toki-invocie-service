from pandas_schema import Column, Schema
from pandas_schema.validation import \
    LeadingWhitespaceValidation, \
    TrailingWhitespaceValidation, \
    MatchesPatternValidation, \
    CustomSeriesValidation
from toki.validation.csv_rules import pandas_is_valid_timestamp

incoming_csv_validation_schema = Schema([
    Column('metering_point_id', [
        MatchesPatternValidation(r"\d{1,10}"),
        LeadingWhitespaceValidation(),
        TrailingWhitespaceValidation()
    ]),
    Column('timestamp', [
        LeadingWhitespaceValidation(),
        TrailingWhitespaceValidation(),
        CustomSeriesValidation(pandas_is_valid_timestamp, 'Invalid timestamp.')
    ]),
    Column('kwh', [
        LeadingWhitespaceValidation(),
        TrailingWhitespaceValidation()
    ]),
])
