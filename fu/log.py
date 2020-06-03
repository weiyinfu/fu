import logging
import sys
from colorlog import ColoredFormatter

simple_formater = logging.Formatter("%(message)s")
default_formatter = logging.Formatter(
    "%(asctime)s %(pathname)s:%(lineno)s %(funcName)s %(process)d [%(name)s]:%(levelname)s %(message)s"
)
colored_formatter = ColoredFormatter(
    "%(asctime)s %(pathname)s:%(lineno)s %(funcName)s [%(name)s]: %(levelname)s %(log_color)s%(message)s%(reset)s"
)

root = logging.root
root.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(colored_formatter)
root.addHandler(console_handler)

console_simple_handler = logging.StreamHandler(sys.stdout)
console_simple_handler.setFormatter(simple_formater)


def getLogger(name) -> logging.Logger:
    return logging.getLogger(name)


def getFileLogger(name, filepath, with_color=False) -> logging.Logger:
    logger = getLogger(name)
    handler = logging.FileHandler(filepath, encoding='utf8')
    handler.setFormatter(default_formatter if not with_color else colored_formatter)
    logger.addHandler(handler)
    return logger
