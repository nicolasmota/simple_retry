def has_retries_to_go(tries_performed, retries_limit):
    return tries_performed < retries_limit


def format_retry_message(
   exception,
   tries_performed,
   retries_limit,
   wait_delay_multiple
):
    message = '{e}, Retrying {tries} of {retries}'.format(
            e=exception,
            tries=tries_performed,
            retries=retries_limit
        )
    if not wait_delay_multiple:
        return message

    return ' '.join([message, 'in {} seconds...'.format(wait_delay_multiple)])


def log_message(
   logger,
   level,
   exception,
   tries_performed,
   retries_limit,
   wait_delay_multiple
):
    if not logger:
        return

    message = format_retry_message(
        exception=exception,
        tries_performed=tries_performed,
        retries_limit=retries_limit,
        wait_delay_multiple=wait_delay_multiple
    )
    getattr(logger, level)(message)
