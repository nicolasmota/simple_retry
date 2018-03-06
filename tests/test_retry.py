from __future__ import absolute_import, unicode_literals

import mock
import pytest

from ..simple_retry.decorators import retry


@retry(Exception, retries=5)
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
