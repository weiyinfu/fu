from fu.concurrent import thread_run


def test_thread_run():
    a = list(range(10))
    ans = thread_run(lambda x: x ** 2, a, show_tqdm=False)
    print(ans)


if __name__ == '__main__':
    test_thread_run()
