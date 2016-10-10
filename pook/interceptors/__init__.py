from .urllib3 import Urllib3Interceptor
from .base import BaseInterceptor  # noqa

# Explicit module exports
__all__ = [
    'store',
    'add',
    'BaseInterceptor'
]

# Store built-in interceptors in pook.
# Note: order is intentional.
store = [
    # UrllibInterceptor,
    Urllib3Interceptor,
    # AIOHTTPInterceptor,
]


def add(interceptor):
    """
    Registers a new HTTP client interceptor.

    Arguments:
        interceptor (interceptor): interceptor class to be added.

    Returns:
        None
    """
    store.append(interceptor)
