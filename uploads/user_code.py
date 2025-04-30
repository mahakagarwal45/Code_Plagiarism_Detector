def bucket_type_key(bucket_type):
    """
    Registers a function that calculates test item key for the specified bucket type.
    """

    def decorator(f):

        @functools.wraps(f)
        def wrapped(item, session):
            key = f(item)

            if session is not None:
                for handler in session.random_order_bucket_type_key_handlers:
                    key = handler(item, key)

            return key

        bucket_type_keys[bucket_type] = wrapped
        return wrapped

    return decorator