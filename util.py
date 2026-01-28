import datetime
from zoneinfo import ZoneInfo


def getNow(time_zone: str):
    if time_zone:
        return datetime.datetime.now(ZoneInfo(time_zone))
    else:
        return datetime.datetime.now()
