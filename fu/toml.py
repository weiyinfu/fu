import toml
import typing

__all__ = ["load", "loads", "dump", "dumps"]


def load(path: str):
    if type(path) == str:
        return toml.load(open(path, encoding="utf8"))
    else:
        return toml.load(path)


def dump(data: object, path: str):
    if type(path) != str:
        toml.dump(data, path)
        return
    with open(path, "w", encoding='utf8') as f:
        toml.dump(data, f)


loads = toml.loads
dumps = toml.dumps
