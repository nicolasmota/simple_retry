import time

from functools import wraps

import asyncio

from simple_retry.simple_retry.helpers import (
    format_retry_message,
    has_retries_to_go,
    log_message
)


def retry(Except, retries=5, delay=0, logger=None, level='info', multiple=1):

    def deco_retry(function):

        @wraps(function)
        def f_retry(*args, **kwargs):
            tries = 1
            mdelay = delay
            while has_retries_to_go(
               tries_performed=tries,
               retries_limit=retries
            ):
                try:
                    return function(*args, **kwargs)
                except Except as e:
                    log_message(
                        logger=logger,
                        level=level,
                        exception=e,
                        tries_performed=tries,
                        retries_limit=retries,
                        wait_delay_multiple=multiple
                    )

                    time.sleep(mdelay)
                    mdelay *= multiple
                    tries += 1
            return function(*args, **kwargs)
        return f_retry
    return deco_retry


def coroutine_retry(
   Except,
   retries=5,
   delay=0,
   logger=None,
   level='info',
   multiple=1
):

    def deco_retry(function):

        @asyncio.coroutine
        @wraps(function)
        def f_retry(*args, **kwargs):
            tries = 1
            mdelay = delay
            while has_retries_to_go(
               tries_performed=tries,
               retries_limit=retries
            ):
                try:
                    return (yield from (function(*args, **kwargs)))
                except Except as e:
                    log_message(
                        logger=logger,
                        level=level,
                        exception=e,
                        tries_performed=tries,
                        retries_limit=retries,
                        wait_delay_multiple=multiple
                    )

                    yield from (asyncio.sleep(mdelay))
                    mdelay *= multiple
                    tries += 1
            return (yield from function(*args, **kwargs))
        return f_retry
    return deco_retry


def async_retry(
   Except,
   retries=5,
   delay=0,
   logger=None,
   level='info',
   multiple=1
):
    def deco_retry(function):

        @wraps(function)
        async def f_retry(*args, **kwargs):
            tries = 1
            mdelay = delay
            while has_retries_to_go(
               tries_performed=tries,
               retries_limit=retries
            ):
                try:
                    return await (function(*args, **kwargs))
                except Except as e:
                    log_message(
                        logger=logger,
                        level=level,
                        exception=e,
                        tries_performed=tries,
                        retries_limit=retries,
                        wait_delay_multiple=multiple
                    )

                    await (asyncio.sleep(mdelay))
                    mdelay *= multiple
                    tries += 1

            return await (function(*args, **kwargs))
        return f_retry
    return deco_retry
