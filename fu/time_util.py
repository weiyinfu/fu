import re
import time
from datetime import datetime
from typing import Union, List

import numpy as np
import pandas as pd
import pytz


def todate(timestamps: List[int], fast=True):
    # 把一个秒数组转成一个日期数组
    if not fast:
        return pd.Series([datetime.fromtimestamp(i) for i in timestamps])
    else:
        return np.array(timestamps, dtype='i8').view('datetime64[s]')


def timestr2second(t: str):
    # 时间字符串转成秒
    if re.match(r"(\d+)-(\d+)-(\d+) (\d+:\d+:\d+)", t):
        return int(datetime.strptime(t, "%Y-%m-%d %H:%M:%S").timestamp())
    if re.match(r'\d+-\d+-\d+T\d+:\d+:\d+\.\d+\+\d+:\d+', t):
        # 2021-04-21T18:45:49.506865102+08:00
        return timestr2second(t[:t.index('.')].replace('T', ' '))


def pdtime2second(t: pd.Timestamp):
    return t.to_pydatetime().timestamp()


def seconds2datetime(seconds: float, utc: bool = False):
    if not utc:
        return datetime.fromtimestamp(seconds)
    x = datetime.fromtimestamp(seconds, pytz.utc)
    return x


def second2str_float(second: float):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(second))


def second2str(seconds: Union[float, List[float]]):
    if type(seconds) in (int, float, np.int32, np.int64, np.float32, np.float64):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds))
    elif type(seconds) == list:
        return [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)) for i in seconds]
    else:
        raise Exception(f"error type {type(seconds)}")


second2str_np = np.frompyfunc(second2str_float, 1, 1)


def second2datetime_np(seconds_array, utc=False):
    return np.array([seconds2datetime(i, utc) for i in seconds_array])


def human_duration(second: float):
    # 把一个时间转成可读性较好的字符串
    second = int(second)
    d = second // (3600 * 24)
    second %= 3600 * 24
    h = second // 3600
    second %= 3600
    m = second // 60
    second %= 60
    s = ""
    if d:
        s += f"{int(d)}天"
    if h:
        s += f"{int(h)}小时"
    if m:
        s += f"{int(m)}分钟"
    if second:
        s += f"{int(second)}秒"
    return s
