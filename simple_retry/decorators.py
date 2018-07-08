import time

from functools import wraps

import asyncio


def retry(Except, retries=5, delay=0, logger=None, level='info', multiple=1):

    def deco_retry(function):

        @wraps(function)
        def f_retry(*args, **kwargs):
            tries = 1
            mdelay = delay
            while tries < retries:
                try:
                    return function(*args, **kwargs)
                except Except as e:
                    msg = '{e}, Retrying {tries} of {retries}'.format(
                        e=e,
                        tries=tries,
                        retries=retries
                    )
                    if mdelay:
                        msg = ' '.join([msg, 'in {} seconds...'.format(mdelay)])
                    if logger:
                        getattr(logger, level)(msg)
                    time.sleep(mdelay)
                    mdelay *= multiple
                    tries += 1
            return function(*args, **kwargs)
        return f_retry
    return deco_retry


def coroutine_retry(Except, retries=5, delay=0, logger=None, level='info', multiple=1):

    def deco_retry(function):

        @asyncio.coroutine
        @wraps(function)
        def f_retry(*args, **kwargs):
            tries = 1
            mdelay = delay
            while tries < retries:
                try:
                    return (yield from (function(*args, **kwargs)))
                except Except as e:
                    msg = '{e}, Retrying {tries} of {retries}'.format(
                        e=e,
                        tries=tries,
                        retries=retries
                    )
                    if mdelay:
                        msg = ' '.join([msg, 'in {} seconds...'.format(mdelay)])
                    if logger:
                        getattr(logger, level)(msg)
                    yield from (asyncio.sleep(mdelay))
                    mdelay *= multiple
                    tries += 1
            return (yield from function(*args, **kwargs))
        return f_retry
    return deco_retry


def async_retry(Except, retries=5, delay=0, logger=None, level='info', multiple=1):
    def deco_retry(function):

        @wraps(function)
        async def f_retry(*args, **kwargs):
            tries = 1
            mdelay = delay
            while tries < retries:
                try:
                    return await (function(*args, **kwargs))
                except Except as e:
                    msg = '{e}, Retrying {tries} of {retries}'.format(
                        e=e,
                        tries=tries,
                        retries=retries
                    )
                    if mdelay:
                        msg = ' '.join([msg, 'in {} seconds...'.format(mdelay)])
                    if logger:
                        getattr(logger, level)(msg)
                    await (asyncio.sleep(mdelay))
                    mdelay *= multiple
                    tries += 1
            return await (function(*args, **kwargs))
        return f_retry
    return deco_retry
