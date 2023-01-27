import subprocess as sp


def get_branches(folder: str):
    """
    获取目录下的branches列表，第一个表示当前branch
    :param folder:
    :return:
    """
    x = sp.check_output("git branch", shell=True, cwd=folder)
    x = str(x, encoding='utf8')
    a = x.splitlines()
    branches = []
    current = ''
    for i in a:
        line = i.strip()
        if line.startswith('*'):
            current = line.strip('*').strip()
        else:
            branches.append(line)
    if not current:
        return []
    return [current] + branches


def get_current_branch(folder: str):
    """
    获取目录的当前branch
    :param folder:
    :return:
    """
    return get_branches(folder)[0]
