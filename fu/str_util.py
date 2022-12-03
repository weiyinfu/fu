import math
import re


def human_size(sz: int):
    # 把一个文件大小转成可读性较好的字符串
    s = 'BkMG'
    x = math.floor(math.log(sz, 1024))
    num = sz / 1024 ** x
    return f"{num:.2f}{s[int(x)]}"


def parse_requirements(filename: str):
    """
    解析requirements.txt
    :return:
    """
    x = open(filename).readlines()
    a = []
    for i in x:
        sep = ""
        if '~=' in i:
            sep = "~="
        elif '==' in i:
            sep = "=="
        if sep:
            name, version = i.split(sep)
        else:
            name = i
        a.append(name)
    return a


def markdown_url(text: str, link: str, ):
    return f"[{text}]({link})"


def get_int_list(s):
    if not s:
        return []
    a = re.split(r'[^\d]', s)
    a = [i.strip() for i in a if i.strip()]
    return [int(i) for i in a]
