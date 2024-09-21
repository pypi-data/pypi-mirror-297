"""
Module
"""

from time import perf_counter

from functools import wraps

def get_time(func: callable) -> callable:
    """
    Wrapps Function and returns execution time

    **Prints:**
    - run_time: float -> the time of the execution of a Function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> any:

        start_time: float = perf_counter()
        result: any = func(*args, **kwargs)
        end_time: float = perf_counter()

        print(
            f"Function {func.__name__} took {end_time - start_time:.3f} seconds to execute"
        )
        return result

    return wrapper
