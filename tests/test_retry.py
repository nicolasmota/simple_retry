from __future__ import absolute_import, unicode_literals

import logging

import asyncio
import mock
import pytest
import os

from ..simple_retry.decorators import retry, coroutine_retry, async_retry

logger = logging.getLogger(__file__)


@retry(Exception, retries=5, delay=1, logger=logger)
def funct_retried():
    os.urandom()
    raise Exception('test')


class TestSimpleRetryDecorator:

    def test_retries_n_times(self):
        with mock.patch('os.urandom') as mock_fun:
            with pytest.raises(Exception):
                funct_retried()
        assert mock_fun.call_count == 5

@asyncio.coroutine
def dumb_coroutine_function():
    os.urandom()


@coroutine_retry(Exception, retries=5, delay=1, logger=logger)
def coroutine_func_retried():
    yield from (dumb_coroutine_function())
    raise Exception('test')


class TestCoroutineSimpleRetryDecorator:

    @pytest.mark.asyncio
    def test_coroutine_retries_n_times(self):
        with mock.patch('os.urandom') as mock_fun:
            with pytest.raises(Exception):
                 yield from (coroutine_func_retried())
        assert mock_fun.call_count == 5


async def dumb_async_function():
    await asyncio.Future()


@async_retry(Exception, retries=5, delay=1, logger=logger)
async def async_func_retried():
    await dumb_async_function()
    raise Exception('test')


class TestAsyncSimpleRetryDecorator:

    @pytest.mark.asyncio
    async def test_async_retries_n_times(self):
        with mock.patch.object(asyncio, 'Future') as mock_fun:
            mock_coro = mock.Mock(name='result', return_value=True)
            mock_fun.side_effect = asyncio.coroutine(mock_coro)

            with pytest.raises(Exception):
                await (async_func_retried())

        assert mock_fun.call_count == 5