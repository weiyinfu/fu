import io
import math

import pylab as plt
from PIL import Image


def get_axes(sz: int):
    # 给定sz，产生一个axes数组
    rows = int(sz ** 0.5)
    cols = math.ceil(sz / rows)
    fig, axes = plt.subplots(rows, cols)
    axes = axes.reshape(-1)
    for i in range(sz, len(axes)):
        axes[i].axis('off')
    return axes[:sz]


def pil_image_to_bytes(img: Image) -> bytes:
    cout = io.BytesIO()
    img.save(cout, format="PNG")
    return cout.getvalue()


def plot2bytes() -> bytes:
    # 画图保存并发送
    cout = io.BytesIO()
    plt.savefig(cout)
    plt.close()
    return cout.getvalue()
