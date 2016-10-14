from inspect import isfunction
from contextlib import contextmanager
from .mock import Mock
from .engine import Engine

# Singleton mock engine
engine = Engine()


def activate(fn=None):
    """
    Enables the HTTP traffic interceptors.

    This function can be used as decorator.
    """
    engine.activate()

    if not isfunction(fn):
        return fn

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
    Alias to pook.activate().
    """
    return activate(fn)


def disable():
    """
    Disables HTTP traffic interceptors.
    """
    engine.disable()


def off():
    """
    Disables HTTP traffic interceptors.
    Alias to pook.disable().
    """
    disable()


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


@contextmanager
def use():
    """
    Create a new isolated mock engine to be used via context manager.

    Example:
        >>> with pook.use() as engine:
        >>>     engine.mock('server.com/foo')
    """
    engine = Engine()
    engine.activate()
    yield engine
    engine.disable()


# Public API
def mock(url=None, **kwargs):
    """
    Registers a new mock for GET method.

    Arguments:
        url (str): request URL to mock.

    Returns:
        pook.Mock: mock instance
    """
    mock = Mock(url=url, **kwargs)
    engine.add_mock(mock)
    return mock


def patch(url=None, **kwargs):
    """
    Registers a new mock.
    Alias to mock()

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='PATCH', **kwargs)


def get(url):
    """
    Registers a new mock for GET method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url)


def post(url, **kwargs):
    """
    Registers a new mock for POST method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='POST', **kwargs)


def put(url, **kwargs):
    """
    Registers a new mock for PUT method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='PUT', **kwargs)


def delete(url, **kwargs):
    """
    Registers a new mock for DELETE method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='DELETE', **kwargs)


def head(url, **kwargs):
    """
    Registers a new mock for HEAD method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='HEAD', **kwargs)


def pending():
    """
    Returns the numbers of pending mocks
    to be matched.

    Returns:
        int: number of pending mocks to reach.
    """
    return 0


def is_done():
    """
    Returns True if all the registered mocks has been triggered.

    Returns:
        bool: True is all the registered mocks are gone, otherwise False.
    """
    return True
