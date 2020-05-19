import requests
from pyquery import PyQuery


def get(url: str, encoding: str, **kwargs) -> PyQuery:
    resp = requests.get(url, **kwargs)
    resp.encoding = encoding
    return PyQuery(resp.text)
