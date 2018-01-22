import time

from functools import wraps


def retry(Except, retries=5, delay=3, logger=None):

    def deco_retry(function):

        @wraps(function)
        def f_retry(*args, **kwargs):
            tries = 1
            while tries < retries:
                try:
                    return function(*args, **kwargs)
                except Except,  e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), delay)
                    if logger:
                        logger.warning(msg)
                    time.sleep(delay)
                    tries += 1
            return function(*args, **kwargs)
        return f_retry
    return deco_retry

