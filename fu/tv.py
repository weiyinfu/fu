"""
time和value的序列
"""
from typing import Dict, List, Union
from typing import Tuple
import numpy as np
import pandas as pd

from bes.idl import idl
from fu import time_util

llint = List[Tuple[int, float]]


def check_format(df: pd.DataFrame):
    assert isinstance(df, pd.DataFrame)
    assert len(df.columns) == 2
    assert list(df.columns.values) == ["timestamp", "value"]


def readable_df(df):
    return pd.DataFrame({
        'timestamp': [time_util.second2str(i) for i in df.timestamp],
        'value': df['value'],
    })


def df2dict(df: pd.DataFrame):
    # dataframe转dict
    if df is None:
        return None
    ans = {}
    for i in df.columns:
        ans[i] = [i if str(i) != 'nan' else None for i in df[i]]
    return ans


def index_of_time(t: Union[float, str], df: pd.DataFrame):
    # 用时间描述的一个字符串，二分查找它在dataframe中的位置下标
    if type(t) == str:
        t = time_util.timestr2second(t)
    a = df['timestamp'].values
    return np.searchsorted(a, t)


def regularize_dataframe(a: pd.DataFrame):
    # 数据类型转换
    if a['value'].dtype != np.float32:
        a['value'] = a['value'].astype(np.float32)
    if a['timestamp'].dtype != np.int32:
        a['timestamp'] = a['timestamp'].astype(np.int32)


def listpoint2dataframe(a: List[idl.Point]):
    """
    把点列表转换成dataframe
    """
    a.sort(key=lambda x: x.Timestamp)  # 此处需要对时间进行排序
    return pd.DataFrame({
        'timestamp': np.array([i.Timestamp for i in a], dtype=np.int32),
        'value': np.array([i.Value for i in a], dtype=np.float32)
    })


def empty_dataframe():
    return pd.DataFrame({
        'timestamp': np.array([], dtype=np.int32),
        'value': np.array([], dtype=np.float32),
    })


def tv2dataframe(t: List[int] or np.ndarray, v: List[float] or np.ndarray):
    return pd.DataFrame({
        'timestamp': np.array(t, dtype=np.int32),
        'value': np.array(v, dtype=np.float32),
    })


def tvdic2df(a: Dict[str, float]):
    if a is None:
        return empty_dataframe()
    a = list([int(t), float(v)] for t, v in a.items())
    a.sort()
    return pd.DataFrame({
        'timestamp': np.array([int(i[0]) for i in a], dtype=np.int32),
        'value': np.array([i[1] for i in a], dtype=np.float32),
    })


def listdict2dataframe(a: List[dict], time_key="timestamp", value_key="value"):
    return pd.DataFrame({
        'timestamp': np.array([i[time_key] for i in a], dtype=np.int32),
        'value': np.array([i[value_key] for i in a], dtype=np.float32),
    })


def llint2df(a: llint):
    return pd.DataFrame({
        'timestamp': np.array([float(i[0]) for i in a], dtype=np.int32),
        'value': np.array([i[1] for i in a], dtype=np.float32)
    })


def df2tvdict(df: pd.DataFrame):
    return {df.iloc[i, 0]: df.iloc[i, 1] for i in range(len(df))}


def df_index2llint(df: pd.DataFrame, bool_index: np.ndarray):
    assert len(df) == len(bool_index)
    return [[df.iloc[i, 0], df.iloc[i, 1]] for i in np.argwhere(bool_index).reshape(-1)]


def dataframe2listpoint(d: pd.DataFrame, class_name=idl.Point):
    """
    把dataframe转成listpoint列表
    """
    ans = []
    for i in range(len(d)):
        p = class_name()
        p.Timestamp = d['timestamp'].iloc[i]
        p.Value = d['value'].iloc[i]
        ans.append(p)
    return ans


def to_prob_list(anoms: pd.DataFrame, a: pd.DataFrame):
    # 把异常点列表转成异常概率数组的形式
    ans = np.zeros(len(a), dtype=np.float32)
    j = 0
    for i in range(len(anoms)):
        while j < len(a) and a['timestamp'].iloc[j] < anoms['timestamp'].iloc[i]:
            j += 1
        if j < len(a):
            ans[j] = 1
    return ans


def dict_df2llint(a: dict):
    # 形如{one:df1,two:df2}这样的字段转成{one:llint1,two:llint2}
    b = {}
    for i in a:
        if type(a[i]) == pd.DataFrame:
            b[i] = df2llint(a[i])
    return b


def df2llint(df: pd.DataFrame):
    return [[int(i['timestamp']), float(i['value'])] for _, i in df.iterrows()]


def df2llint_pretty(df: pd.DataFrame):
    # 把dataframe的时间列转成字符串
    return [
        [time_util.second2str(i['timestamp']), float(i['value'])] for _, i in df.iterrows()
    ]
