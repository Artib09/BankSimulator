import functools
import time


def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__
        print(f"[{name}] Starting execution")

        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        print(f"[{name}] Executed in {elapsed:.4f} s")
        return result
    return wrapper