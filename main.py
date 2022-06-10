import os

from config import DATA_DIR
from utils.api_caller import RecordType
from utils.data_utils import json_to_csv


def prepare_csv_file(record_type: RecordType):
    raw_file = os.path.join(DATA_DIR, f'raw_{record_type.name}.txt')
    csv_file = os.path.join(DATA_DIR, f'raw_{record_type.name}.csv')
    json_to_csv(raw_file, csv_file, 'timestr', 'time', 'open', 'close', 'low', 'high', 'volumefrom', 'volumeto')


# prepare_csv_file(RecordType.HOURLY)
# prepare_csv_file(RecordType.DAILY)
