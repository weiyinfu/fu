import json

import numpy as np
from flask import json as json2

from bes.util import dict_obj

"""
json.dumps()可以通过实现一个class或者使用default函数两种方式来定制
"""


def patch(json):
    old_dumps = json.dumps
    old_dump = json.dump

    def dumps(*args, **kwargs):
        if 'default' not in kwargs and 'cls' not in kwargs:
            kwargs['default'] = dict_obj.todict
        kwargs['allow_nan'] = True
        return old_dumps(*args, **kwargs)

    def dump(*args, **kwargs):
        if 'default' not in kwargs and 'cls' not in kwargs:
            kwargs['default'] = dict_obj.todict
        kwargs['allow_nan'] = True
        return old_dump(*args, **kwargs)

    json.dumps = dumps
    json.dump = dump


patch(json)
patch(json2)
if __name__ == '__main__':
    a = np.array([1, 2, 3, 4])
    b = {
        'one': a,
        'd': a[0],
        'two': np.NAN,
    }
    s = json.dumps(b)
    print(s)
    print(json.loads(s))
