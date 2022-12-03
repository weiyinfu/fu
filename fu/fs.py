import os


def ensure_dir(folder: str):
    # 保证文件夹的存在
    if not (os.path.exists(folder) and os.path.isdir(folder)):
        os.makedirs(folder)


def home(sub_path=''):
    # 获取home目录
    HOME = os.path.abspath(os.environ['HOME'])
    return os.path.join(HOME, sub_path)


def listdir(folder: str):
    # listdir但是忽略以.开头的文件名
    return [i for i in os.listdir(folder) if not i.startswith('.')]

