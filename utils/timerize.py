from functools import wraps
import time
from colorama import Fore, Style, init

init(autoreset=True)

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(Fore.LIGHTBLUE_EX + f'Function {func.__name__} took {total_time:.2f} seconds' + Style.RESET_ALL)
        return result
    return timeit_wrapper