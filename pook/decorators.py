import functools


def fluent(fn):
    """
    Method decorator to allow easy method chaining.
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kw):
        # Create a copy of the class instance attribute
        # s = self.__class__.__new__(self.__class__)
        # s.__dict__ = self.__dict__.copy()
        # Trigger method proxy
        result = fn(self, *args, **kw)
        # Return self instance or method result
        return self if result is None else result
    return wrapper
