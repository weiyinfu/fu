import pickle

import zstandard

decoder = zstandard.ZstdDecompressor()
encoder = zstandard.ZstdCompressor(level=zstandard.MAX_COMPRESSION_LEVEL)


def compress_pickle(obj):
    return encoder.compress(pickle.dumps(obj))


def decompress_pickle(data: bytes):
    if data is None:
        return None
    res = decoder.decompress(data)
    return pickle.loads(res)
