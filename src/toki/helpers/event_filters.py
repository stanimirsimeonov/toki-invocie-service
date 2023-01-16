from toki.dto.models_new_csv_files import S3BucketFile
import re


def filter_event_initial_uploaded_files(event) -> bool:
    """
    The given method will filter events only to the bucket responsible for  the new files
    """
    return event.EventName == 's3:ObjectCreated:Put' and re.match(r'new\-files\/(.*)', event.Key)

def filter_event_valid_moved_files(event) -> bool:
    """
    The given method will filter events only to the bucket responsible for the valid files
    """
    return event.EventName == 's3:ObjectCreated:Copy' and re.match(r'valid\-files\/(.*)', event.Key)


def filter_event_valid_files_for_invoices(event) -> bool:
    """
    The given method will filter events only to the bucket responsible for the valid files ready for invoices
    """
    return event.EventName == 's3:ObjectAccessed:Head' and re.match(r'pre\-invoice\-raw\-files\/(.*)', event.Key)
