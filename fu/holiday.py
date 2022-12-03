import os
import re
from datetime import datetime
from functools import lru_cache
from typing import Optional, Callable

"""
# Holiday数据格式
holiday文件夹中表示各个年份的法定节假日数据。
`1.1-1.3` 表示1月1日、1月2日、1月3日这三天为假期。
`1.1-1.1` 表示1月1日为假期
如果没有“-”，单独一行1.4表示1月4日是工作日。
也就是说，如果包含“-”，表示一个时间段，表示放假时间，这是一个前闭后闭区间。
如果不包含“-”，表示一个时间点，表示工作时间，这是一个时间点。

举个例子：`1.1-1.5`（周一到周五）放了五天假，1.6和1.7（周六周日）需要补课，那么就写成：
```
1.1-1.5
1.6
1.7
```
"""
work_day = []
from_year, end_year = -1, -1
lack_data_alarm: Optional[Callable] = None


def is_leap_year(year: int):
    # 判断年份是否是闰年
    if year % 100 == 0:
        return int(year / 100) % 4 == 0
    else:
        return year % 4 == 0


def get_month_days(month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month == 2:
        return 28
    else:
        return 30


@lru_cache(maxsize=2)
def get_year_data(year: int):
    folder = os.path.dirname(os.path.abspath(__file__))
    fpath = os.path.join(folder, f"{year}.txt")
    if not os.path.exists(fpath):
        if lack_data_alarm:
            lack_data_alarm(year)
        return []
    with open(fpath) as f:
        lines = f.readlines()
    lines = [i.strip() for i in lines if i.strip()]
    ans = []
    for j in lines:
        if '-' in j:
            res = re.search(r'(\d+)\.(\d+)-(\d+)\.(\d+)', j)
            fm, fd, tm, td = [int(res.group(i + 1)) for i in range(4)]
            ans.append((fm, fd, tm, td))
        else:
            m, d = j.split('.')
            ans.append((m, d))
    return ans


def is_holiday(timestamp: float):
    d = datetime.fromtimestamp(timestamp)
    data = get_year_data(d.year)
    if d.weekday() in (5, 6):  # 如果是周末
        for i in data:
            if len(i) == 2:
                # 如果是周末上班
                month, day = i
                if d.month == month and d.day == day:
                    return False
        return True
    else:
        # 如果是周一到周五，
        for i in data:
            if len(i) == 4:
                fm, fd, tm, td = i
                if (tm, td) >= (d.month, d.day) >= (fm, fd):
                    return True
        return False


if __name__ == '__main__':
    from time import time

    print(is_holiday(time() - 3 * 24 * 3600))
