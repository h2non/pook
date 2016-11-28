import sys
from .urllib3 import Urllib3Interceptor
from .http import HTTPClientInterceptor
from .base import BaseInterceptor

# Explicit symbols to export
__all__ = (
    'interceptors', 'add', 'get',
    'BaseInterceptor',
    'Urllib3Interceptor',
    'HTTPClientInterceptor',
    'AIOHTTPInterceptor',
)

# Store built-in interceptors in pook.
interceptors = [
    Urllib3Interceptor,
    HTTPClientInterceptor
]

# Import aiohttp in modern Python runtimes
if sys.version_info >= (3, 4, 2):
    from .aiohttp import AIOHTTPInterceptor
    interceptors.append(AIOHTTPInterceptor)


def add(*interceptors):
    """
    Registers a new HTTP client interceptor.

    Arguments:
        *interceptors (interceptor): interceptor(s) to be added.
    """
    interceptors.append(*interceptors)


def get(name):
    """
    Returns an interceptor by class name.

    Arguments:
        name (str): interceptor class name or alias.

    Returns:
        interceptor: found interceptor instance, otherwise ``None``.
    """
    for interceptor in interceptors:
        if interceptor.__name__ == name:
            return interceptor
