"""
fetch all bitcoin records from online source (https://min-api.cryptocompare.com/documentation)
save raw data in .txt file
"""
import json
import os.path

from config import DATA_DIR
from utils.api_caller import HistoricalBTCRecord, RecordType
from utils.time_utils import to_timestamp, to_datetime_str

start_datetime = "2022-01-01 00:00:00"
caller = HistoricalBTCRecord()


def get_records(record_type: RecordType, append=False):
    """
    get all record and save to (fixed) data file
    each line is a record
    :param record_type: daily or hourly
    :param append: append to existed file or write a new one
    :return:
    """
    output_file = os.path.join(DATA_DIR, f'raw_{record_type.name}.txt')
    write_mode = 'a' if append else 'w'
    f = open(output_file, write_mode)
    remove_chars = len(os.linesep)

    count = 0
    from_ts = to_timestamp(start_datetime)
    for record in caller.fetch_records_in_time_period(record_type=record_type, from_ts=from_ts):
        record['timestr'] = to_datetime_str(record['time'])
        f.write(json.dumps(record))
        f.write('\n')
        count += 1

        if count % 100 == 0:
            f.flush()  # flush file buffer each 100 records

    f.truncate(f.tell() - remove_chars)  # remove the last empty line
    f.close()

    print(f'fetched {count} records, saved data to file: {output_file}')


# usage: uncomment to start crawl data
# get_records(record_type=RecordType.DAILY)
# get_records(record_type=RecordType.HOURLY)
