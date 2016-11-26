import functools


def fluent(fn):
    """
    Method decorator to allow easy method chaining.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kw):
        # Trigger method proxy
        result = fn(self, *args, **kw)
        # Return self instance or method result
        return self if result is None else result
    return wrapper
