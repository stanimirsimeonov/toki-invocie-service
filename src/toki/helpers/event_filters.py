# from toki.dto.models_new_csv_files import S3BucketFile
import re


def filter_event_initial_uploaded_files(event) -> bool:
    """
    The given method will filter events only to the bucket responsible for  the new files
    """
    if event.EventName == 's3:ObjectCreated:Put' and re.match(r'new\-files\/(.*)', event.Key):
        return True


def filter_event_valid_moved_files(event) -> bool:
    """
    The given method will filter events only to the bucket responsible for the valid files
    """
    if event.EventName == 's3:ObjectCreated:Put' and re.match(r'valid\-files\/(.*)', event.Key):
        return True
