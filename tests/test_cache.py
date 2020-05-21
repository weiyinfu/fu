from fu import cache
import time
from unittest import TestCase


class TestCache(TestCase):
    def test1(self):
        @cache.simple_cache(timeout=1)
        def haha():
            print('haha is called')
            return time.time()

        haha()
        haha()
        time.sleep(2)
        haha()
        print(cache.get_cache(haha))
        cache.remove(haha)
        print(cache.get_cache(haha))
