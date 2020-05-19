import json
import typing

__all__ = ["load", "loads", "dump", "dumps"]


def load(path: str):
    if type(path) == str:
        return json.load(open(path, encoding="utf8"))
    else:
        return json.load(path)


def dump(data: object, path: str, **kwargs):
    if type(path) != str:
        json.dump(data, path, **kwargs)
        return
    with open(path, "w", encoding='utf8') as f:
        kwargs['ensure_ascii'] = False
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
