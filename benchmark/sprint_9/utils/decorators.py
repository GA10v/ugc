from functools import wraps
from time import time


def timer(resul_message: str, batch: int = None):
    def timer_decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            start = time()
            func(*args, **kwargs)
            stop = time()
            func_time = stop - start
            if batch:
                print('====' * 10)
                print(f'- Batch size: {batch} items;')
            print(resul_message, f'выполнена за {round(func_time, 5)}')

        return _wrapper

    return timer_decorator
