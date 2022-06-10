import datetime


def current_timestamp():
    return int(datetime.datetime.now().timestamp())


def to_timestamp(datetime_str: str):
    """
    convert datetime in string format to timestamp
    :param datetime_str: e.g '2022-06-09 08:15:27'
    """
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').replace(
        tzinfo=datetime.timezone.utc).timestamp().as_integer_ratio()[0]


def to_datetime_str(timestamp: int):
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


# print(to_timestamp('2022-06-09 16:00:00'))
# print(to_datetime_str(to_timestamp('2022-06-09 16:00:00')))
# print(current_timestamp())
# print(to_datetime_str(current_timestamp()))
