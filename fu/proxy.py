import fastapi
import requests
from flask import Response, Request
import logging

"""
根据flask的request构建flask的response，用于动态路由转发
"""


def get_flask_response(url: str, request: Request, timeout=None):
    req_headers = {key: value for (key, value) in request.headers if key.lower != 'host'}
    resp = requests.request(method=request.method,
                            url=url,
                            headers=req_headers,
                            data=request.data,
                            stream=True, timeout=timeout)
    resp_headers = []
    for name, value in resp.headers.items():
        if name.lower() in ('content-length',
                            'transfer-encoding',
                            'connection',
                            'content-encoding'):
            continue
        resp_headers.append((name, value))
    return Response(resp.content, status=resp.status_code, headers=resp_headers)


async def get_fastapi_response(url: str, request: fastapi.Request, timeout=None):
    req_headers = {key: value for (key, value) in request.headers.items() if key.lower() != 'host'}
    req_headers['connection'] = "keep-alive"
    del req_headers['accept-encoding']
    content = await request.body()
    resp = requests.request(method=request.method,
                            url=url,
                            headers=req_headers,
                            data=content,
                            stream=True, timeout=timeout)
    resp_headers = []
    logging.info(f"doing {request.method} to {url} statusCode={resp.status_code} headers={req_headers}")
    for name, value in resp.headers.items():
        if name.lower() in (
                'content-length',
                'transfer-encoding',
                'connection',
                'content-encoding'
        ):
            continue
        resp_headers.append((name, value))
    return fastapi.Response(resp.content, status_code=resp.status_code, headers={k: v for k, v in resp_headers})
