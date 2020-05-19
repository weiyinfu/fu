建立自己的python库，都是一些惯用法。  
安装方法`pip install .`，使用`python setup.py install`会产生一堆没用的build文件。  


关闭进程：`lsof -i:8080| awk 'NR>1 {print $$2}'| uniq  | xargs kill -9`