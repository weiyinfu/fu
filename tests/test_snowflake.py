from fu import snow_flake
import unittest


class TestSnowFlake(unittest.TestCase):
    def setUp(self) -> None:
        self.snow = snow_flake.SnowFlake()

    def tearDown(self) -> None:
        pass

    def testGenerate(self):
        a = [self.snow.get_id() for _ in range(10)]
        assert len(a) == len(set(a))
        assert type(a[0]) == int
        print(a)
