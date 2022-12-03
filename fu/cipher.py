import hashlib
from typing import Union


def md5(s: Union[str, bytes]):
    # 计算md5字符串
    x = hashlib.md5(bytes(s, 'utf8') if type(s) == str else s)
    res = x.hexdigest()
    return res
