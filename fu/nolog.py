import logging
from typing import List


class NoLog:
    # 暂时关闭日志
    def __init__(self, loggers: List[logging.Logger]):
        self.old_level = []
        self.loggers = loggers

    def __enter__(self):
        self.old_level = [i.level for i in self.loggers]
        for i in self.loggers:
            i.setLevel(logging.WARNING)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for ind, i in enumerate(self.loggers):
            i.setLevel(self.old_level[ind])
