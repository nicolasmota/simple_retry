from __future__ import absolute_import, unicode_literals

import logging
import mock
import pytest

from ..simple_retry.decorators import retry

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
