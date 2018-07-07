from __future__ import absolute_import, unicode_literals

import logging

import asyncio
import mock
import pytest


from ..simple_retry.decorators import retry, coroutine_retry

logger = logging.getLogger(__file__)


@retry(Exception, retries=5, delay=1, logger=logger)
def funct_retried():
    import os
    os.urandom()
    raise Exception('test')


class TestSimpleRetryDecorator:

    def test_retries_n_times(self):
        with mock.patch('os.urandom') as mock_fun:
            with pytest.raises(Exception):
                funct_retried()
        assert mock_fun.call_count == 5


@coroutine_retry(Exception, retries=5, delay=1, logger=logger)
def coroutine_func_retried():
    yield from asyncio.sleep(1)
    raise Exception('test')


class TestCoroutineSimpleRetryDecorator:

    def test_coroutine_retries_n_times(self):
        with mock.patch('asyncio.sleep') as mock_fun:
            with pytest.raises(Exception):
                 yield from (coroutine_func_retried())
        assert mock_fun.call_count == 5