import random
import string
from functools import wraps


def retry(exceptions: object | tuple, max_retries: int = 1):
    """
    Retry function on exceptions caught.
    :param exceptions: exceptions caught
    :param max_retries: number of retries
    """
    def deco_retry(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            tries = 0
            while tries < max_retries-1:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    tries += 1
            return func(*args, **kwargs)
        return func_retry
    return deco_retry


def get_random_string(length: int = 10) -> str:
    """
    Generates random string from given length.
    :param length: default length to 10
    :return: random string
    """
    return ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(length))
