import enum
from typing import Generator, Dict, List

import requests

from config import *
from utils.time_utils import current_timestamp, to_datetime_str


class RecordType(enum.Enum):
    DAILY = 'histoday'
    HOURLY = 'histohour'


class HistoricalBTCRecord:
    def __init__(self):
        self.api_header = self.__build_header()
        # self.prefix_url =

    @staticmethod
    def __build_header() -> dict:
        """
        build header message for request, API KEY is included here
        :return: header as dict
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': f"Apikey {API_KEY}"
        }
        return headers

    @staticmethod
    def __build_request_url(record_type: RecordType, **kwargs):
        base_url = f"{API_PREFIX}/{record_type.value}?fsym={FSYM}&tsym={TSYM}"

        for k, v in kwargs.items():  # append additional params for the call
            base_url = f'{base_url}&{k}={v}'
        print('build url:', base_url)

        return base_url

    def single_fetch(self, record_type: RecordType, to_ts=None, limit=2000) -> List[Dict]:
        """
        get historical records before timestamp `to_ts`, maximum is 2000 records
        :param record_type: daily or hourly
        :param to_ts: if None, use current timestamp
        :param limit: number of records want to fetch
        :return:
        """
        params = {'limit': limit}
        if to_ts:
            params['toTs'] = to_ts

        url = self.__build_request_url(record_type, **params)
        data = requests.get(url, headers=self.api_header)

        if data.status_code != 200:
            raise Exception(f'call failed, message:{data.text}')

        records = json.loads(data.text)['Data']['Data']
        return records

    def fetch_records_in_time_period(self, record_type: RecordType, from_ts, to_ts=None) -> Generator:
        """
        get all possible records during the time period
        default return the newest record first (recommend to avoid save large records in memory)
        :param record_type: daily or hourly
        :param from_ts: the oldest timestamp
        :param to_ts: if None, use current ts

        :return: a generator of records
        """
        cur_to_ts = to_ts if to_ts else current_timestamp()
        print(f'Start fetching records from {to_datetime_str(from_ts)} to {to_datetime_str(cur_to_ts)}')
        while cur_to_ts > from_ts:
            print(to_datetime_str(cur_to_ts))
            records = self.single_fetch(record_type=record_type, to_ts=cur_to_ts)
            if len(records) == 0:
                print('Empty response!')
                break

            records.sort(key=lambda x: x['time'], reverse=True)  # newest first
            cur_to_ts = records[-1]['time']  # track the oldest time for next fetch
            print(to_datetime_str(records[-1]['time']), to_datetime_str(records[0]['time']))

            for record in records:  # the first record is the newest
                if record['time'] < from_ts:  # reached the oldest time point
                    break
                yield record


# sample:
caller = HistoricalBTCRecord()
caller.single_fetch(RecordType.DAILY, limit=5)
