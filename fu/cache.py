import json
import time

"""
functools中的缓存不支持强制刷新，自己实现一个支持强制刷新的缓存接口

完备好用的cache，可以设置有效次数、有效时长
"""


def simple_cache(timeout=None):
    """
    简单cache装饰器
    :param timeout:超时时间
    :return:
    """
    def decorator(f):
        def ff(*args, **kwargs):
            key = get_key(*args, **kwargs)
            res = ff.cache.get(key)

            def go():
                res = {"last_time": time.time(), "data": f(*args, **kwargs)}
                ff.cache[key] = res
                return res['data']

            if not res:
                return go()
            # 如果超时了
            last_time = res['last_time']
            if timeout is not None and time.time() - last_time > timeout:
                return go()
            return res["data"]

        ff.cache = {}

        def get_key(*args, **kwargs):
            return json.dumps([args, kwargs])

        ff.get_key = get_key

        return ff

    return decorator


def get_cache(f):
    """
    获取缓存函数的全部缓存对象
    :param f:
    :return:
    """
    return f.cache


def clear_cache(f):
    """
    清空全部缓存
    :param f:
    :return:
    """
    f.cache.clear()


def remove(f, *args, **kwargs):
    """
    删除缓存中的某个缓存
    :param f:
    :param args:
    :param kwargs:
    :return:
    """
    k = f.get_key(*args, **kwargs)
    if k not in f.cache:
        return
    del f.cache[k]
