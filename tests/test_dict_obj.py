from fu.dict_obj import DictObj


def test_one():
    x = DictObj({'one': 1, 'two': 2})
    print(x)
    print(x.keys())
    import pickle

    print(pickle.dumps(x))
