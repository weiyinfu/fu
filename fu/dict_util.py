"""
字典工具函数
"""


def reverse_nvn(one2many):
    """
    把多对多映射变成多对多映射
    :param one2many: dict(x->list)
    :return:
    """
    a = dict()
    for i in one2many:
        for j in one2many[i]:
            if j not in a:
                a[j] = set()
            a[j].add(i)
    for i in a:
        a[i] = list(a[i])
    return a


def reverse_1v1(one2one):
    # 把一对一映射翻转一下
    return dict((i[1], i[0]) for i in one2one.items())


def reverse_1vn(one2many):
    # 把一对多映射变成多对一映射
    a = dict()
    for i in one2many:
        for j in one2many[i]:
            a[j] = i
    return a
