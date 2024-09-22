from time import perf_counter
# from functools import wraps

def time_function(func):

    # @wraps(func)
    def wrapper(*args, **kwargs):
        ts = perf_counter()
        result = func(*args, **kwargs)
        te = perf_counter()
        # print(te - ts)
        # print(f'{func.__name__} = {(te - ts) :015.10f}')
        return result, te - ts

    return wrapper

