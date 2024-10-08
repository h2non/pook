from .base import BaseInterceptor
from .http import HTTPClientInterceptor
from .urllib3 import Urllib3Interceptor

# Explicit symbols to export
__all__ = (
    "interceptors",
    "add",
    "get",
    "BaseInterceptor",
    "Urllib3Interceptor",
    "HTTPClientInterceptor",
    "HttpxInterceptor",
    "AIOHTTPInterceptor",
)

# Store built-in interceptors in pook.
interceptors = [Urllib3Interceptor, HTTPClientInterceptor]

try:
    import aiohttp  # noqa
    from .aiohttp import AIOHTTPInterceptor

    interceptors.append(AIOHTTPInterceptor)
except ImportError:
    pass

try:
    import httpx  # noqa
    from ._httpx import HttpxInterceptor

    interceptors.append(HttpxInterceptor)
except ImportError:
    pass


def add(*custom_interceptors):
    """
    Registers a new HTTP client interceptor.

    Arguments:
        *custom_interceptors (interceptor): interceptor(s) to be added.
    """
    interceptors.append(*custom_interceptors)


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
