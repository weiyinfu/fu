from collections import Iterable
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


def thread_run(f, args_list, max_workers=10, show_tqdm=True, tqdm_desc: str = ""):
    """
    这个函数相比ThreadPoolExecutor.map的优势在于，它能够显示进度条
    :param f:
    :param args_list:
    :param max_workers:
    :param show_tqdm:
    :param tqdm_desc:
    :return:
    """
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = []
        for args in args_list:
            if isinstance(args, list) or isinstance(args, tuple):
                real_args = args
            else:
                real_args = (args,)
            tasks.append(pool.submit(f, *real_args))
        pool.shutdown()
        if show_tqdm:
            tasks = tqdm(tasks, desc=tqdm_desc)
        else:
            tasks = tasks
        result = []
        for i in tasks:
            result.append(i.result())
        return result
