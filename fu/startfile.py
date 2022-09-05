import os
import sys
import subprocess as sp


def startfile(filename):
    if sys.platform == 'darwin':
        sp.check_call(['open', filename])
    else:
        os.startfile(filename)
