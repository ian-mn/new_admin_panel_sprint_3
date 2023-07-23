import inspect
import math
from functools import wraps
from time import sleep

from logger import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=100):
    """Exponential backoff decorator if function fails.

    Args:
        start_sleep_time (float, optional): Sleep time on first try. Defaults to 0.1.
        factor (int, optional): Factors sleep time after each try. Defaults to 2.
        border_sleep_time (int, optional): Maximum sleep time. Defaults to 100.
    """

    def decorator_backoff(func):
        @wraps(func)
        def wrapper_backoff_generator(*args, **kwargs):
            n = 0
            while True:
                try:
                    for i in func(*args, **kwargs):
                        yield i
                    break
                except Exception as e:
                    logger.error(e)
                    backoff_sleep(start_sleep_time, factor, border_sleep_time, n)
                    n += 1

        @wraps(func)
        def wrapper_backoff(*args, **kwargs):
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    backoff_sleep(start_sleep_time, factor, border_sleep_time, n)
                    n += 1

        if inspect.isgenerator(func):
            return wrapper_backoff_generator
        return wrapper_backoff

    return decorator_backoff


def backoff_sleep(start_sleep_time, factor, border_sleep_time, n) -> None:
    """Sleeps for
    t = start_sleep_time * factor ^ n if t < border_sleep_time
    t = border_sleep_time if t >= border_sleep_time
    """

    t = start_sleep_time * math.pow(factor, n)
    if t >= border_sleep_time:
        t = border_sleep_time
    logger.error(f"Backoff for {round(t)} seconds")
    sleep(t)
