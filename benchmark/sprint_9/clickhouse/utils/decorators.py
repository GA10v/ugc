from time import time
from functools import wraps


def timer(resul_message: str):
    def timer_decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            start = time()
            func(*args, **kwargs)
            stop = time()
            func_time = stop - start
            print(resul_message, f'выполнена за {round(func_time, 5)}')
        return _wrapper
    return timer_decorator
