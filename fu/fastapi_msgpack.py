import typing

import msgpack
from fastapi import Response

from fu import dict_obj


def msgpackify(data):
    return msgpack.dumps(data, default=dict_obj.todict)


class MsgpackResponse(Response):
    media_type = "application/x-msgpack"

    def render(self, content: typing.Any) -> bytes:
        return msgpackify(content)
