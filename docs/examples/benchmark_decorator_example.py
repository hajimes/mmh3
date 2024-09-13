import time
from functools import wraps


def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter_ns()
        res = func(*args, **kwargs)
        t2 = time.perf_counter_ns() - t1
        print(f"{func.__name__}: {t2} nanoseconds")
        return res

    return wrapper


@benchmark
def add(a, b):
    return a + b


# output example: "add: 459 nanoseconds"
add(1, 2)
