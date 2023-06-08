"""
使dict像python对象一样可以通过点来访问
"""
from datetime import datetime

import numpy as np
import pandas as pd


class DictObj(dict):
    def __init__(self, dic=None):
        super(dict, self).__init__()
        if dic:
            for k, v in dic.items():
                self[k] = v

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        # 没有getstate和setstate就无法执行pickle
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)


def todict(obj):
    if obj is None:
        return None
    elif type(obj) in (int, float, str, complex, bool):
        return obj
    elif isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                          np.int16, np.int32, np.int64, np.uint8,
                          np.uint16, np.uint32, np.uint64,)):

        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)

    elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
        return {'real': obj.real, 'imag': obj.imag}

    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()

    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (bytes,)):
        return str(obj)
    elif isinstance(obj, (np.void)):
        return None
    elif isinstance(obj, (datetime,)):
        try:
            return obj.timestamp()
        except ValueError:
            return None
    elif isinstance(obj, (pd.Series,)):
        return obj.tolist()
    elif isinstance(obj, (pd.DataFrame,)):
        return {k: todict(obj[k]) for k in obj.columns}
    elif callable(obj):
        # 如果obj是一个可调用的对象
        return None
    elif hasattr(obj, 'to_json') and callable(getattr(obj, 'to_json')):
        return getattr(obj, 'to_json')()
    elif type(obj) == list:
        ans = []
        for i in obj:
            ans.append(todict(i))
        return ans
    elif type(obj) == dict:
        return {k: todict(v) for k, v in obj.items()}
    elif isinstance(obj, (object,)):
        ans = {}
        for i in dir(obj):
            if i.startswith('_'):
                continue
            if not hasattr(obj, i):
                continue
            v = getattr(obj, i)
            if v == obj:
                continue
            if callable(v):
                continue
            ans[i] = todict(v)
        return ans
    raise TypeError(f'Object of type {obj.__class__.__name__} '
                    f'is not JSON serializable')


