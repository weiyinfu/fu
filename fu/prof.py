import cProfile
import pstats
import subprocess as sp
import tempfile
import webbrowser
from os.path import *

from fu import time_util

"""
python性能分析工具：可以指定folder，只看folder下面的那些结点
"""


def run(statement: str, folder=None, filename: str = None):
    pro = cProfile.Profile()
    pro.enable()
    pro.run(statement)
    pro.disable()
    sta = pstats.Stats(pro)
    folder = abspath(folder)

    def is_good(filepath: str):
        if filepath.startswith("<"):
            return False
        if filepath == '~':
            return False
        if not abspath(filepath).startswith(folder):
            return False
        return True

    def rewrite_stats():
        ans = {}
        if folder is None:
            return
        for k, v in sta.stats.items():
            filepath, line, func = k
            if not is_good(filepath):
                continue
            son_dic = {}
            for son_k, son_v in v[4].items():
                if not is_good(son_k[0]):
                    continue
                son_dic[son_k] = son_v
            v = list(v)
            v[4] = son_dic
            v = tuple(v)
            ans[k] = v
        sta.stats = ans

    rewrite_stats()
    if filename:
        sta.dump_stats(filename)
        return sta
    sta.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    folder = tempfile.gettempdir()
    stats_path = join(folder, 'haha.stats')
    html_path = join(folder, 'index.html')
    png_path = join(folder, 'prof.png')
    sta.dump_stats(stats_path)
    png_rel_path = relpath(png_path, dirname(html_path))
    open(html_path, 'w').write(f"""
<html>
    <head></head>
    <body>
        <img src="{png_rel_path}">
    </body>
</html>
        """)
    sp.check_call(f"gprof2dot -f pstats {stats_path} | dot -Tpng -o {png_path}", shell=True)
    webbrowser.open_new_tab(f"file://{html_path}")
    return sta


"""
usage:
def go():
    from time import time
    print(time_util.second2str(time()))

run('go()', "xxxx_folder")

"""
