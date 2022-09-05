import json
import os

from tqdm.autonotebook import tqdm
from fu import json
from fu import xml2json

"""
数据清洗：把博客园数据导出
首先以xml格式导出博客园数据
然后把xml转换成json
children,label,url
"""


def main(src_path, target_folder):
    blog = open(src_path).read()
    res = xml2json.xml2json(blog)
    res = json.loads(res)
    items = res["rss"]["channel"]["item"]

    blog_dir = target_folder
    print(blog_dir)
    if not os.path.exists(blog_dir):
        os.mkdir(blog_dir)
    """
    建立倒排索引
    """
    for ind, i in enumerate(tqdm(items)):
        target_path = os.path.join(blog_dir, str(ind) + ".json")
        del i["guid"]
        del i["creator"]
        i["content"] = i["description"]
        del i["description"]
        k = os.path.basename(i["link"])
        if k in a:
            i["path"] = a[k]
        json.dump(i, target_path)
