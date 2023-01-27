import os
import signal
import sys

"""
让进程接收ctrl+c信号
"""


def term1(sig_num, addtion):
    print("term is called")
    os.killpg(os.getpgid(os.getpid()), signal.SIGKILL)


term = term1


def prepare():
    signal.signal(signal.SIGTERM, term)
    signal.signal(signal.SIGINT, term)
