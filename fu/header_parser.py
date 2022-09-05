def parse_header(header_string: str):
    head = {}
    for i in header_string.splitlines():
        i = i.strip()
        if not i.strip():
            continue
        if i.startswith(':'):
            continue
        ind = i.index(':')
        k, v = i[:ind], i[ind + 1:]
        k = k.strip()
        v = v.strip()
        head[k] = v
    return head


if __name__ == '__main__':
    print(parse_header("""
    :authority: rosetta.feishu.cn
:method: GET
:path: /rosetta/api/v1/products/29/cdn
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8
cache-control: no-cache
origin: https://bytedance.feishu.cn
pragma: no-cache
referer: https://bytedance.feishu.cn/drive/folder/fldcnbBk4QXvPYz4ZVLtKXnhC0Q
sec-fetch-mode: cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
x-tt-bes: bes_new
    """))
