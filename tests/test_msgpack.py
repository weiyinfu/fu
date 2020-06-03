from fu import msgpack as m
a={'one':1,'two':'three'}
s=m.dumps(a)
print(s)
m.dump()