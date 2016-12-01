import functools


def fluent(fn):
    """
    Simple function decorator allowing easy method chaining.

    Arguments:
        fn (function): target function to decorate.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kw):
        # Trigger method proxy
        result = fn(self, *args, **kw)
        # Return self instance or method result
        return self if result is None else result
    return wrapper
