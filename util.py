# -*- coding: utf-8 -*-
import datetime
import locale
import time

from PIL import Image
import numpy as np


def _get_local_tz():
    EPOCH = datetime.datetime(1970, 1, 1)
    OS_ENCODING = locale.getdefaultlocale()[1]

    local_datetime = datetime.datetime(*time.localtime(0)[:6])
    dst = time.daylight and local_datetime.tm_isdst > 0
    gmtoff = -(time.altzone if dst else time.timezone)

    time_delta = local_datetime - EPOCH

    if time_delta == datetime.timedelta(seconds=gmtoff):
        tz_name = time.tzname[dst].encode('charmap').decode(OS_ENCODING)
        tz = datetime.timezone(time_delta, tz_name)
    else:
        tz = datetime.timezone(time_delta)

    return tz


class TimeManager(object):
    TIMEZONE_KR = datetime.timezone(datetime.timedelta(0, 32400), 'Asia/Seoul')
    TIMEZONE_UTC = datetime.timezone.utc
    TIMEZONE_LOCAL = _get_local_tz()

    @staticmethod
    def _get_utc_datetime():
        return datetime.datetime.utcnow(). \
            replace(tzinfo=TimeManager.TIMEZONE_UTC)

    @staticmethod
    def _get_kr_datetime():
        return TimeManager._get_utc_datetime(). \
            astimezone(TimeManager.TIMEZONE_KR)

    @staticmethod
    def get_now_datetime(utc=False):
        return TimeManager._get_utc_datetime() if utc else TimeManager._get_kr_datetime()

    @staticmethod
    def formatted_today(utc=False) -> str:
        dt = TimeManager._get_utc_datetime() if utc else TimeManager._get_kr_datetime()
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def formatted_now(utc=False) -> str:
        dt = TimeManager._get_utc_datetime() if utc else TimeManager._get_kr_datetime()
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def str_to_timestamp(formatted_str: str, utc=False) -> int:
        dt = TimeManager.str_to_datetime(formatted_str, utc)
        timetuple = dt.timetuple()
        return time.mktime(timetuple)

    @staticmethod
    def str_to_datetime(formatted_str: str, utc=False) -> datetime.datetime:
        tz = TimeManager.TIMEZONE_UTC if utc else TimeManager.TIMEZONE_KR
        return datetime.datetime. \
            strptime(formatted_str, "%Y-%m-%d %H:%M:%S"). \
            replace(tzinfo=tz)

    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime.datetime:
        return datetime.datetime. \
            fromtimestamp(timestamp). \
            replace(tzinfo=TimeManager.TIMEZONE_LOCAL)

    @staticmethod
    def to_KR(dt: datetime.datetime) -> datetime.datetime:
        return dt.astimezone(TimeManager.TIMEZONE_KR)

    @staticmethod
    def to_UTC(dt: datetime.datetime) -> datetime.datetime:
        return dt.astimezone(TimeManager.TIMEZONE_UTC)


def sharpness(img_path):
    im = Image.open(img_path).convert('L')  # to grayscale
    array = np.asarray(im, dtype=np.int32)

    gy, gx = np.gradient(array)
    gnorm = np.sqrt(gx ** 2 + gy ** 2)
    return np.average(gnorm)
