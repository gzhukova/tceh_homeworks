import timeit
from contextlib import contextmanager


class Lock(object):
    def __init__(self):
        self.lock = False
    def __enter__(self):
        self.lock = True
        return self.lock
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("self.lock - change")


@contextmanager
def all_exceptions():
    """
    Контекстны менеджер, перехватывающий исключения и пишущий их в консоль
    :return: None
    """
    try:
        yield
    except Exception as ex:
        print("logs: ", ex.__class__.__name__)
    finally:
        print('Done!')

@contextmanager
def time_dimension():
    """
    Контекстный менеджер измерения времени выполнения блока кода
    :return: None
    """
    start_time = timeit.default_timer()
    yield
    print("Execution time was: {0}".format(timeit.default_timer() - start_time))

def some_long_function():
    s = [x for x in range(100)]
    return s


if __name__ == '__main__':
    #Задача №1
    with Lock() as lock:
        print(lock)
    # Задача №2
    with all_exceptions():
        1 / 0
    #Задача №3
    with time_dimension():
        s = some_long_function()

