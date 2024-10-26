from functools import wraps
import time
from colorama import Fore, Style, init
import logging
from constants.constants import DEBUG_LEVEL

init(autoreset=True)
logging.basicConfig(
    filename="logging/app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=DEBUG_LEVEL
)

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(Fore.LIGHTBLUE_EX + f'Function {func.__name__} took {total_time:.2f} seconds' + Style.RESET_ALL)
        logging.debug(f'Function {func.__name__} took {total_time:.2f} seconds')
        return result
    return timeit_wrapper