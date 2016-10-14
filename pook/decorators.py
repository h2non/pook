import functools


def fluent(fn):
    """
    Method decorator to allow easy method chaining.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        return self if result is None else result
    return wrapper
