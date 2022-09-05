"""
把confluence格式的wiki以html格式导出

把html格式的confluence文件转换成json
author
title
link
description
pubDate
path
"""

import json
import os

import pyquery as pq
from tqdm.autonotebook import tqdm


def parse(file: str):
    # 把一个html格式的文件转换成json格式
    html = open(file).read()
    doc = pq.PyQuery(html)
    breadcrumbs = doc("#breadcrumbs a")
    path = [i.text for i in breadcrumbs]
    content = doc("#main-content").html().strip()
    meta = doc("#content .page-metadata").text()
    title = doc("#title-heading").text()
    title = title.replace("魏印福(实习) : ", "")
    return {
        "title": title,
        "meta": meta,
        "content": content,
        "path": path,
        "link": file,
    }


def main(src_file, des_file):
    if not os.path.exists(des_file):
        os.mkdir(des_file)
    for i in tqdm(os.listdir(src_file)):
        src = os.path.join(src_file, i)
        if os.path.isfile(src):
            res = parse(src)
            des = os.path.join(des_file, i + ".json")
            json.dump(res, open(des, "w"), ensure_ascii=0, indent=2)
