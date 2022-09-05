import msgpack

__all__ = ["load", "loads", "dump", "dumps"]


def load(path: str):
    if type(path) == str:
        return msgpack.load(open(path, encoding="utf8"))
    else:
        return msgpack.load(path)


def dump(data: object, path: str):
    if type(path) != str:
        msgpack.dump(data, path)
        return
    with open(path, "wb") as f:
        msgpack.dump(data, f)


loads = msgpack.loads
dumps = msgpack.dumps
