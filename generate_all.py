"""

生成all.py

"""
from os.path import *
import os

a = []
for i in os.listdir("fu"):
    if i.endswith(".py") and not i.startswith("__"):
        pkg, _ = splitext(i)
        if pkg == 'all':
            continue
        a.append(pkg)
a = [f"from . import {i}" for i in a]
content = '\n'.join(a)
open("fu/all.py", 'w').write(content)
