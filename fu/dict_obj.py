"""
使dict像python对象一样可以通过点来访问
"""


class DictObj(dict):
    def __init__(self, dic=None):
        super(dict, self).__init__()
        if dic:
            for k, v in dic.items():
                self[k] = v

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value


if __name__ == '__main__':
    x = DictObj({'one': 1, 'two': 2})
    print(x)
    print(x.keys())
