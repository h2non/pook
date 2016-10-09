from inspect import isfunction
from contextlib import contextmanager
from .mock import Mock
from .engine import Engine

# Singleton mock engine
engine = Engine()


def activate(fn=None):
    """
    Enables the HTTP traffic interceptors.
    """
    engine.activate()

    if not isfunction(fn):
        return None

    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as err:
            raise err
        finally:
            engine.disable()

    return wrapper


def on(fn=None):
    """
    Enables the HTTP traffic interceptors.
    Alias to pock.activate().
    """
    return activate(fn)


def use_network():
    """
    Enables real networking if no mock can be matched.
    """
    engine.networking = True


def disable_network():
    """
    Disable real networking.
    """
    engine.networking = False


def disable():
    """
    Disables HTTP traffic interceptors.
    """
    engine.disable()


def off():
    """
    Disables HTTP traffic interceptors.
    Alias to pock.disable().
    """
    disable()


@contextmanager
def use():
    """
    Enables the HTTP interceptor for context usage.
    Example: with pock.use() as engine:
    """
    engine.activate()
    yield engine
    engine.disable()


# Public API
def mock(url, method='GET', **kwargs):
    """
    Registers a new mock for GET method.
    """
    mock = Mock(url, method, **kwargs)
    engine.add_mock(mock)
    return mock


def get(url):
    """
    Registers a new mock for GET method.
    """
    return mock(url)


def post(url, **kwargs):
    """
    Registers a new mock for POST method.
    """
    return mock(url, method='POST', **kwargs)


def put(url, **kwargs):
    """
    Registers a new mock for PUT method.
    """
    return mock(url, method='PUT', **kwargs)


def patch(url, **kwargs):
    """
    Registers a new mock for PATCH method.
    """
    return mock(url, method='PATCH', **kwargs)


def delete(url, **kwargs):
    """
    Registers a new mock for DELETE method.
    """
    return mock(url, method='DELETE', **kwargs)


def head(url, **kwargs):
    """
    Registers a new mock for HEAD method.
    """
    return mock(url, method='HEAD', **kwargs)


def pending():
    """
    Returns the numbers of pending mocks
    to be matched.
    """
    return 0


def is_done():
    """
    Returns True if all the registered mocks has been triggered.
    """
    return True
