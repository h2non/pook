import functools
import re
from contextlib import contextmanager
from inspect import isfunction

from .engine import Engine
from .matcher import MatcherEngine
from .mock import Mock
from .mock_engine import MockEngine
from .request import Request
from .response import Response

try:
    from asyncio import iscoroutinefunction
except ImportError:
    iscoroutinefunction = None
if iscoroutinefunction is not None:
    from .activate_async import activate_async
else:
    activate_async = None

# Public API symbols to export
__all__ = (
    'activate', 'on', 'disable', 'off', 'reset', 'engine',
    'use_network', 'enable_network', 'disable_network',
    'get', 'post', 'put', 'patch', 'head', 'use',
    'set_mock_engine', 'delete', 'options', 'pending',
    'ispending', 'mock', 'pending_mocks', 'unmatched_requests',
    'isunmatched', 'unmatched', 'isactive', 'isdone', 'regex',
    'Engine', 'Mock', 'Request', 'Response',
    'MatcherEngine', 'MockEngine', 'use_network_filter'
)

# Default singleton mock engine to be used
_engine = Engine()


def debug(enable=True):
    """
    Enables or disables debug mode in the current mock engine.

    Arguments:
        enable (bool): ``True`` to enable debug mode. Otherwise ``False``.
    """
    _engine.debug = enable


def engine():
    """
    Returns the current running mock engine.

    Returns:
        pook.Engine: current used engine.
    """
    return _engine


def set_mock_engine(engine):
    """
    Sets a custom mock engine, replacing the built-in one.

    This is particularly useful if you want to replace the built-in
    HTTP traffic mock interceptor engine with your custom one.

    For mock engine implementation details, see `pook.MockEngine`.

    Arguments:
        engine (pook.MockEngine): custom mock engine to use.
    """
    _engine.set_mock_engine(engine)


def activate(fn=None):
    """
    Enables the HTTP traffic interceptors.

    This function can be used as decorator.

    Arguments:
        fn (function|coroutinefunction): Optional function argument
            if used as decorator.

    Returns:
        function: decorator wrapper function, only if called as decorator,
            otherwise ``None``.

    Example::

        # Standard use case
        pook.activate()
        pook.mock('server.com/foo').reply(404)

        res = requests.get('server.com/foo')
        assert res.status_code == 404
        pook.disable()

        # Decorator use case
        @pook.activate
        def test_request():
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    # If not used as decorator, activate the engine and exit
    if not isfunction(fn):
        _engine.activate()
        return None

    # If used as decorator for an async coroutine, wrap it
    if iscoroutinefunction is not None and iscoroutinefunction(fn):
        return activate_async(fn, _engine)

    @functools.wraps(fn)
    def wrapper(*args, **kw):
        _engine.activate()
        try:
            fn(*args, **kw)
        finally:
            _engine.disable()

    return wrapper


def on(fn=None):
    """
    Enables the HTTP traffic interceptors.
    Alias to ``pook.activate()``.

    Arguments:
        fn (function|coroutinefunction): Optional function argument
            if used as decorator.

    Returns:
        function: decorator wrapper function, only if called as decorator.

    Example::

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
    _engine.disable()


def off():
    """
    Disables mock engine, HTTP traffic interceptors and flushed all the
    registered mocks.

    Internally, it calls ``pook.disable()`` and ``pook.off()``.
    """
    disable()
    reset()


def reset():
    """
    Resets current mock engine state, flushing all the registered mocks.

    This action will not disable the mock engine.
    """
    _engine.reset()


@contextmanager
def use(network=False):
    """
    Creates a new isolated mock engine to be used via context manager.

    Example::

        with pook.use() as engine:
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    global _engine

    # Create temporal engine
    __engine = _engine
    activated = __engine.active
    if activated:
        __engine.disable()

    _engine = Engine(network=network)
    _engine.activate()

    # Yield enfine to be used by the context manager
    yield _engine

    # Restore engine state
    _engine.disable()
    if network:
        _engine.disable_network()

    # Restore previous engine
    _engine = __engine
    if activated:
        _engine.activate()


@contextmanager
def context(network=False):
    """
    Create a new isolated mock engine to be used via context manager.

    Semantic alias to ``pook.context()``.

    Example::

        with pook.use() as engine:
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    with use(network=network) as engine:
        yield engine


@contextmanager
def use_network():
    """
    Creates a new mock engine to be used as context manager

    Example::

        with pook.use_network() as engine:
            pook.mock('server.com/foo').reply(404)

            res = requests.get('server.com/foo')
            assert res.status_code == 404
    """
    with use(network=True) as engine:
        yield engine


def enable_network(*hostnames):
    """
    Enables real networking mode for unmatched mocks in the current
    mock engine.
    """
    _engine.enable_network(*hostnames)


def disable_network():
    """
    Disables real traffic networking mode in the current mock engine.
    """
    _engine.disable_network()


def use_network_filter(*fn):
    """
    Adds network filters to determine if certain outgoing
    unmatched HTTP traffic can stablish real network connections.

    Arguments:
        *fn (function): variadic function filter arguments to be used.
    """
    _engine.use_network_filter(*fn)


def flush_network_filters():
    """
    Flushes registered real networking filters in the current
    mock engine.
    """
    _engine.flush_network_filters()


def mock(url=None, **kw):
    """
    Creates and register a new HTTP mock.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic keyword arguments.

    Returns:
        pook.Mock: mock instance
    """
    return _engine.mock(url, **kw)


def get(url, **kw):
    """
    Registers a new mock HTTP request with GET method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='GET', **kw)


def post(url, **kw):
    """
    Registers a new mock HTTP request with POST method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='POST', **kw)


def put(url, **kw):
    """
    Registers a new mock HTTP request with PUT method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='PUT', **kw)


def delete(url, **kw):
    """
    Registers a new mock HTTP request with DELETE method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='DELETE', **kw)


def head(url, **kw):
    """
    Registers a new mock HTTP request with HEAD method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

    Returns:
        pook.Mock: mock instance
    """
    return mock(url, method='HEAD', **kw)


def patch(url=None, **kw):
    """
    Registers a new mock HTTP request with PATCH method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

    Returns:
        pook.Mock: new mock instance.
    """
    return mock(url, method='PATCH', **kw)


def options(url=None, **kw):
    """
    Registers a new mock HTTP request with OPTIONS method.

    Arguments:
        url (str): request URL to mock.
        activate (bool): force mock engine activation.
            Defaults to ``False``.
        **kw (mixed): variadic arguments to ``pook.Mock`` constructor.

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
    return _engine.pending()


def ispending():
    """
    Returns the numbers of pending mocks to be matched.

    Returns:
        int: number of pending mocks to match.
    """
    return _engine.ispending()


def pending_mocks():
    """
    Returns pending mocks to be matched.

    Returns:
        list: pending mock instances.
    """
    return _engine.pending_mocks()


def unmatched_requests():
    """
    Returns a ``tuple`` of unmatched requests.

    Unmatched requests will be registered only if ``networking``
    mode has been enabled.

    Returns:
        list: unmatched intercepted requests.
    """
    return _engine.unmatched_requests()


def unmatched():
    """
    Returns the total number of unmatched requests intercepted by pook.

    Unmatched requests will be registered only if ``networking``
    mode has been enabled.

    Returns:
        int: total number of unmatched requests.
    """
    return _engine.unmatched()


def isunmatched():
    """
    Returns ``True`` if there are unmatched requests. Otherwise ``False``.

    Unmatched requests will be registered only if ``networking``
    mode has been enabled.

    Returns:
        bool
    """
    return _engine.isunmatched()


def isactive():
    """
    Returns ``True`` if pook is active and intercepting traffic.
    Otherwise ``False``.

    Returns:
        bool: True is all the registered mocks are gone, otherwise False.
    """
    return _engine.isactive()


def isdone():
    """
    Returns True if all the registered mocks has been triggered.

    Returns:
        bool: True is all the registered mocks are gone, otherwise False.
    """
    return _engine.isdone()


def regex(expression, flags=re.IGNORECASE):
    """
    Convenient shortcut to ``re.compile()`` for fast, easy to use
    regular expression compilation without an extra import statement.

    Arguments:
        expression (str): regular expression value.
        flags (int): optional regular expression flags.
            Defaults to ``re.IGNORECASE``

    Returns:
        expression (str): string based regular expression.

    Raises:
        Exception: in case of regular expression compilation error

    Example::

        (pook
            .get('api.com/foo')
            .header('Content-Type', pook.regex('[a-z]{1,4}')))
    """
    return re.compile(expression, flags=flags)
