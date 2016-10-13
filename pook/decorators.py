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


def expectation(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'expectations'):
            self.expectations = {}

        try:
            return fn(self, *args, **kwargs)
        finally:
            name = fn.__name__
            store = self.expectations.get(name)
            if not store:
                store = []
            store.append(*args)
            self.expectations[name] = store

    return wrapper
