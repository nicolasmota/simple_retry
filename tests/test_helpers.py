from simple_retry.simple_retry.helpers import format_retry_message, has_retries_to_go


class TestRetryHelpers:

    def test_should_create_message_with_multiple(self):
        msg = format_retry_message(
            exception=ValueError('A dumb error'),
            tries_performed=2,
            retries_limit=5,
            wait_delay_multiple=1
        )

        assert msg == 'A dumb error, Retrying 2 of 5 in 1 seconds...'

    def test_should_create_message_without_multiple(self):
        msg = format_retry_message(
            exception=ValueError('A dumb error'),
            tries_performed=2,
            retries_limit=5,
            wait_delay_multiple=0
        )

        assert msg == 'A dumb error, Retrying 2 of 5'

    def test_has_retries_to_go_should_return_true_when_smaller_than_limit(
       self
    ):
        assert has_retries_to_go(tries_performed=4, retries_limit=5) is True

    def test_has_retries_to_go_should_return_true_when_reaches_limit(
       self
    ):
        assert has_retries_to_go(tries_performed=4, retries_limit=4) is False

