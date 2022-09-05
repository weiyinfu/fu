import logging
import sys
from colorlog import ColoredFormatter

# formatters
simple_formater = logging.Formatter("%(message)s")
default_formatter = logging.Formatter(
    "%(asctime)s %(pathname)s:%(lineno)s %(funcName)s %(process)d [%(name)s]:%(levelname)s %(message)s"
)
colored_formatter = ColoredFormatter(
    "%(asctime)s %(pathname)s:%(lineno)s %(funcName)s [%(name)s]: %(levelname)s %(log_color)s%(message)s%(reset)s"
)
# handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(colored_formatter)
console_handler.setLevel(logging.INFO)


# loggers
root = logging.root
root.setLevel(logging.INFO)
root.addHandler(console_handler)
