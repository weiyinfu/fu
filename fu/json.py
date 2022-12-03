import json
import typing
from typing import Union

__all__ = ["load", "loads", "dump", "dumps"]

FilePathOrFile = Union[str, typing.IO[str]]


def load(path: FilePathOrFile):
    if type(path) == str:
        return json.load(open(path, encoding="utf8"))
    else:
        return json.load(path)


def dump(data: object, path: FilePathOrFile, **kwargs):
    if type(path) != str:
        if 'ensure_ascii' not in kwargs:
            kwargs['ensure_ascii'] = False
        if 'indent' not in kwargs:
            kwargs['indent'] = 2
        json.dump(data, path, **kwargs)
        return
    with open(path, "w", encoding='utf8') as f:
        if 'ensure_ascii' not in kwargs:
            kwargs['ensure_ascii'] = False
        if 'indent' not in kwargs:
            kwargs['indent'] = 2
        json.dump(data, f, **kwargs)


def read_lines(filepath: str):
    with open(filepath, "r", encoding='utf8') as f:
        for line in f:
            yield json.loads(line)


def write_lines(lines: typing.List[dict], dstpath: str):
    with open(dstpath, "w", encoding='utf8') as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")


loads = json.loads
dumps = json.dumps
