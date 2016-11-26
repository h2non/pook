import re
import functools
from inspect import isfunction
from contextlib import contextmanager
from .engine import Engine

from .mock import Mock  # noqa
from .request import Request  # noqa
from .response import Response  # noqa

# Explicit symbols to export (analog to __all__)
api_exports = (
    'activate', 'on', 'disable', 'off', 'engine',
    'use_network', 'enable_network', 'use', 'mock',
    'get', 'post', 'put', 'patch', 'head',
    'delete', 'options', 'pending', 'ispending',
    'pending_mocks', 'unmatched_requests', 'isunmatched',
    'unmatched', 'isactive', 'isdone', 'regex',
    'Engine', 'Mock', 'Request', 'Response'
)

# Default singleton mock engine to be used
engine = Engine()


def activate(fn=None):
    """
    Enables the HTTP traffic interceptors.

    This function can be used as decorator.

    Arguments:
        fn (function): Optional function argument if used as decorator.

    Returns:
        function: decorator wrapper function, only if called as decorator.

    Usage::

        # Standard usage
        pook.activate()
        pook.mock('server.com/foo').reply(404)

        res = requests.get('server.com/foo')
        assert res.status_code == 404

        # Usage as decorator
        @pook.activate
        def test_request():
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    engine.activate()

    if not isfunction(fn):
        return None

    @functools.wraps(fn)
    def wrapper(*args, **kw):
        try:
            fn(*args, **kw)
        except Exception as err:
            raise err
        finally:
            engine.disable()

    return wrapper


def on(fn=None):
    """
    Enables the HTTP traffic interceptors.
    Alias to ``pook.activate()``.

    Arguments:
        fn (function): Optional function argument if used as decorator.

    Returns:
        function: decorator wrapper function, only if called as decorator.

    Usage::

        # Standard usage
        pook.on()
        pook.mock('server.com/foo').reply(404)

        res = requests.get('server.com/foo')
        assert res.status_code == 404

        # Usage as decorator
        @pook.on
        def test_request():
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
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
    Alias to ``pook.disable()``.
    """
    disable()


@contextmanager
def use_network():
    """
    Creates a new mock engine to be used as context manager

    Usage::

        with pook.use_network() as engine:
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    with use(network=True) as engine:
        yield engine


def enable_network(*hostnames):
    """
    Enables real networking if no mock can be matched.
    """
    engine.enable_network(*hostnames)


def disable_network():
    """
    Disables real traffic networking mode.
    """
    engine.disable_network()


@contextmanager
def use(network=False):
    """
    Create a new isolated mock engine to be used via context manager.

    Usage::

        with pook.use() as engine:
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    global engine

    # Create temporal engine
    _engine = engine
    activated = _engine.active
    if activated:
        engine.disable()

    engine = Engine(network=network)
    engine.activate()

    # Yield enfine to be used by the context manager
    yield engine

    # Restore engine state
    engine.disable()
    if network:
        engine.disable_network()

    # Restore previous engine
    engine = _engine
    if activated:
        engine.activate()


def mock(url=None, **kw):
    """
    Creates and register a new HTTP mock.

    Arguments:
        url (str): request URL to mock.
        **kw (mixed): variadic keyword arguments.

    Returns:
        pook.Mock: mock instance
    """
    return engine.mock(url, **kw)


def get(url, **kw):
    """
    Registers a new mock for GET method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='GET', **kw)


def post(url, **kw):
    """
    Registers a new mock for POST method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='POST', **kw)


def put(url, **kw):
    """
    Registers a new mock for PUT method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='PUT', **kw)


def delete(url, **kw):
    """
    Registers a new mock for DELETE method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='DELETE', **kw)


def head(url, **kw):
    """
    Registers a new mock for HEAD method.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='HEAD', **kw)


def patch(url=None, **kw):
    """
    Creates a new mock for the given URL. Alias to `mock()`.

    Returns:
        pook.Mock: new mock instance.
    """
    return mock(url, method='PATCH', **kw)


def options(url=None, **kw):
    """
    Creates a new mock for the given URL with the OPTIONS HTTP verb.
    Alias to `mock()`.

    Returns:
        pook.Mock: new mock instance.
    """
    return mock(url, method='OPTIONS', **kw)


def pending():
    """
    Returns the numbers of pending mocks to be matched.

    Returns:
        int: number of pending mocks to match.
    """
    return engine.pending()


def ispending():
    """
    Returns the numbers of pending mocks to be matched.

    Returns:
        int: number of pending mocks to match.
    """
    return engine.ispending()


def pending_mocks():
    """
    Returns pending mocks to be matched.

    Returns:
        list: pending mock instances.
    """
    return engine.pending_mocks()


def unmatched_requests():
    """
    Returns a ``tuple`` of unmatched requests.

    Unmatched requests will be registered only if ``networking``
    mode has been enabled.

    Returns:
        tuple: unmatched intercepted requests.
    """
    return engine.unmatched_requests()


def unmatched():
    """
    Returns the total number of unmatched requests intercepted by pook.

    Unmatched requests will be registered only if ``networking``
    mode has been enabled.

    Returns:
        int: total number of unmatched requests.
    """
    return engine.unmatched()


def isunmatched():
    """
    Returns ``True`` if there are unmatched requests. Otherwise ``False``.

    Unmatched requests will be registered only if ``networking``
    mode has been enabled.

    Returns:
        bool
    """
    return engine.isunmatched()


def isactive():
    """
    Returns ``True`` if pook is active and intercepting traffic.
    Otherwise ``False``.

    Returns:
        bool: True is all the registered mocks are gone, otherwise False.
    """
    return engine.isactive()


def isdone():
    """
    Returns True if all the registered mocks has been triggered.

    Returns:
        bool: True is all the registered mocks are gone, otherwise False.
    """
    return engine.isdone()


def regex(expression, flags=re.IGNORECASE):
    """
    Convenient shortcut to ``re.compile()`` for fast, easy to use
    regular expression compilation.

    Returns:
        expression (str): string regular expression.

    Raises:
        Exception: in case of regular expression compilation error

    Usage::

        (pook
            .get('api.com/foo')
            .header('Content-Type', pook.regex('[a-z]{1,4}')))
    """
    return re.compile(expression, flags=flags)
