import pickle

"""
允许一个对象从另外一个对象进行复制

让自定义的类继承Unpickle这个类，就能够实现安全的unpickle，从而把pickle变成一种序列化方式
"""


class Unpickle:
    # 此类的作用有两个：一个是tojson，另一个是unpickle，具备加载另一个对象的属性的能力
    def unpickles(self, x: bytes):
        self.from_another(pickle.loads(x))

    def unpickle(self, filepath: str):
        content = open(filepath, 'rb').read()
        self.unpickles(content)

    def from_another(self, x):
        for i in dir(x):
            if i.startswith('_'):
                continue
            if not hasattr(self, i):
                continue
            v = getattr(x, i)
            if callable(v):
                continue
            setattr(self, i, v)

    def to_json(self):
        ans = {}
        for i in dir(self):
            if i.startswith('_'):
                continue
            if not hasattr(self, i):
                continue
            v = getattr(self, i)
            if callable(v):
                continue
            ans[i] = v
        return ans
