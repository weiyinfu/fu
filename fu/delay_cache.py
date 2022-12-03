import pickle
import time
from functools import lru_cache
import wrapt

"""
delay_cache是一个函数注解工具，当调用参数相同的时候，在一段时间内直接返回结果，不执行函数
"""


class DelayCache(object):
    def __init__(self, delay_s):
        self.delay_s = delay_s
        self.start_time = 0
        self.tick = 0

    @wrapt.decorator
    def __call__(self, func, instance, args, kwargs):
        self.func = func
        self.args, self.kwargs = args, kwargs
        if time.time() - self.start_time > self.delay_s:
            self.tick ^= 1  # 状态切换，相当于自锁开关
        hashable_arg = pickle.dumps((self.tick, args, kwargs))
        return self.delay_cache(hashable_arg)

    @lru_cache(maxsize=1)
    def delay_cache(self, _):
        self.start_time = time.time()  # 计时复位
        return self.func(*self.args, **self.kwargs)


@DelayCache(3)
def test_delay_cache(name):
    print('called', name)


if __name__ == '__main__':
    test_delay_cache('weiyinfu')
    test_delay_cache('weiyinfu')
    time.sleep(3)
    test_delay_cache('weiyinfu')
