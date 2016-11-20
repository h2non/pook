from .urllib3 import Urllib3Interceptor
from .aiohttp import AIOHTTPInterceptor
from .http import HTTPClientInterceptor
from .base import BaseInterceptor  # noqa


# Store built-in interceptors in pook.
# Note: order is intentional.
interceptors = [
    Urllib3Interceptor,
    AIOHTTPInterceptor,
    HTTPClientInterceptor
]


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
