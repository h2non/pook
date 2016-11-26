import re
import functools
from inspect import isfunction, ismethod
from .decorators import fluent
from .response import Response
from .request import Request
from .matcher import MatcherEngine
from .helpers import trigger_methods
from .exceptions import PookExpiredMock
from .matchers import init as matcher  # noqa


def _append_funcs(target, items):
    """
    Helper function to append functions into a given list.

    Arguments:
        target (list): receptor list to append functions.
        items (iterable): iterable that yields elements to append.
    """
    [target.append(item) for item in items
     if isfunction(item) or ismethod(item)]


def _trigger_request(instance, request):
    """
    Triggers request mock definition methods dynamically based on input
    keyword arguments passed to `pook.Mock` constructor.

    This is used to provide a more Pythonic interface vs chainable API
    approach.
    """
    if not isinstance(request, Request):
        raise TypeError('request must be instance of pook.Request')

    # Register request matchers
    for key in request.keys:
        if hasattr(instance, key):
            getattr(instance, key)(getattr(request, key))


class Mock(object):
    """
    Mock is used to declare and compose the HTTP request/response mock
    definition and matching expectations, which provides fluent API DSL.
    """

    def __init__(self, request=None, response=None, **kw):
        # Stores the number of times the mock should live
        self._times = 1
        # Stores the number of times the mock has been matched
        self._matches = 0
        # Stores the simulated error exception
        self._error = None
        # Stores the optional network delay in milliseconds
        self._delay = 0
        # Stores the mock persistance mode. `True` means it will live forever
        self._persist = False
        # Stores the input request instance
        self._request = request
        # Stores the response mock instance
        self._response = response or Response()
        # Stores the mock matcher engine used for outgoing traffic matching
        self.matchers = MatcherEngine()
        # Stores filters used to filter outgoing HTTP requests.
        self.filters = []
        # Stores HTTP request mappers used by the mock.
        self.mappers = []
        # Stores callback functions that will be triggered if the mock
        # matches outgoing traffic.
        self.callbacks = []

        # Triggers instance methods based on argument names
        trigger_methods(self, kw)

        # Trigger request fields, if present
        if request:
            _trigger_request(self, request)

    @fluent
    def protocol(self, value):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('URLProtocolMatcher', value))

    @fluent
    def url(self, url):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('URLMatcher', url))

    @fluent
    def method(self, method):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('MethodMatcher', method))

    @fluent
    def path(self, path):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('PathMatcher', path))

    @fluent
    def header(self, name, value):
        """
        Returns:
            self: current Mock instance.
        """
        headers = (name, value)
        self.add_matcher(matcher('HeadersMatcher', *headers))

    @fluent
    def headers(self, headers=None, **kw):
        """
        Returns:
            self: current Mock instance.
        """
        headers = kw if kw else headers
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def header_present(self, name):
        """
        Returns:
            self: current Mock instance.
        """
        headers = {name: re.compile('(.*)')}
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def headers_present(self, headers):
        """
        Returns:
            self: current Mock instance.
        """
        headers = {name: re.compile('(.*)') for name in headers}
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def type(self, value):
        """
        Returns:
            self: current Mock instance.
        """
        self.content(value)

    @fluent
    def content(self, value):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('HeadersMatcher', {'Content-Type': value}))

    @fluent
    def param(self, name, value):
        """
        Returns:
            self: current Mock instance.
        """
        self.params({name: value})

    @fluent
    def param_exists(self, name):
        """
        Returns:
            self: current Mock instance.
        """
        self.params({name: re.compile('(.*)')})

    @fluent
    def params(self, params):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('QueryMatcher', params))

    @fluent
    def body(self, body):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('BodyMatcher', body))

    @fluent
    def json(self, body):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('JSONMatcher', body))

    @fluent
    def json_schema(self, schema):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('JSONSchemaMatcher', schema))

    @fluent
    def file(self, path):
        """
        Reads the body to match from a disk file.

        Returns:
            self: current Mock instance.
        """
        with open(path, 'r') as f:
            self.body(str(f.read()))

    @fluent
    def xml(self, body):
        """
        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('XMLMatcher', body))

    @fluent
    def add_matcher(self, matcher):
        """
        Returns:
            self: current Mock instance.
        """
        self.matchers.add(matcher)

    @fluent
    def use(self, *matchers):
        """
        Returns:
            self: current Mock instance.
        """
        [self.add_matcher(matcher) for matcher in matchers]

    @fluent
    def times(self, num=1):
        """
        Returns:
            self: current Mock instance.
        """
        self._times = num

    @fluent
    def persist(self):
        """
        Returns:
            self: current Mock instance.
        """
        self._persist = True

    @fluent
    def filter(self, *filters):
        """
        Returns:
            self: current Mock instance.
        """
        _append_funcs(self.filters, filters)

    @fluent
    def map(self, *mappers):
        """
        Returns:
            self: current Mock instance.
        """
        _append_funcs(self.mappers, mappers)

    @fluent
    def callback(self, *callbacks):
        """
        Returns:
            self: current Mock instance.
        """
        _append_funcs(self.callbacks, callbacks)

    @fluent
    def delay(self, delay=1000):
        """
        Delay network response with certain milliseconds.
        Only supported by asynchronous HTTP clients, such as ``aiohttp``.

        Arguments:
            delay (int): milliseconds to delay response.

        Returns:
            self: current Mock instance.
        """
        self._delay = int(delay)

    @fluent
    def error(self, error):
        """
        Defines a simulated exception error that will be raised.

        Returns:
            self: current Mock instance.
        """
        self._error = RuntimeError(error) if isinstance(error, str) else error

    def reply(self, status=200, **kw):
        """
        Defines the mock response.

        Returns:
            pook.Response: mock response definition instance.
        """
        # Use or create a Response mock instance
        res = self._response or Response(**kw)
        # Define HTTP mandatory response status
        res.status = status or res.status
        # Expose current mock instance in response for self-reference
        res.mock = self
        # Define mock response
        self._response = res
        # Return response
        return res

    def status(self, code=200):
        """
        Defines the response status code.
        Equivalent to ``self.reply(code)``.

        Arguments:
            code (int): response status code. Defaults to ``200``.

        Returns:
            pook.Response: mock response definition instance.
        """
        return self.reply(status=code)

    def response(self, status=200, **kw):
        """
        Defines the mock response. Alias to ``.reply()``

        Returns:
            pook.Response: mock response definition instance.
        """
        return self.reply(status=status, **kw)

    def isdone(self):
        """
        Returns ``True`` if the mock has been matched by outgoing HTTP traffic.

        Returns:
            bool: ``True`` if the mock was matched succesfully.
        """
        return (self._persist and self._matches > 0) or self._times <= 0

    def __call__(self, fn):
        """
        Overload Mock instance as callable object in order to be used
        as decorator definition syntax.
        """
        # Support chain sequences of mock definitions
        if isinstance(fn, Response):
            return fn.mock
        if isinstance(fn, Mock):
            return fn

        # Force type assertion and raise an error if it is not a function
        if not isfunction(fn) and not ismethod(fn):
            raise TypeError('first argument must be a method or function')

        @functools.wraps(fn)
        def wrapper(*args, **kw):
            return fn(*args, **kw)

        return wrapper

    def match(self, request):
        """
        Matches an outgoing HTTP request against the current mock matchers.

        This method acts like a delegator to `pook.MatcherEngine`.

        Raises:
            Exception: if the mock has an exception defined.

        Returns:
            bool: `True` if the mock matches the outgoing HTTP request,
                otherwise `False`.
        """
        if self._times <= 0:
            raise PookExpiredMock('Mock expired')

        # Trigger mock filters
        for test in self.filters:
            if not test(request, self):
                return False

        # Trigger mock mappers
        for mapper in self.mappers:
            request = mapper(request, self)
            if not request:
                raise ValueError('map function must return a request object')

        # Match incoming request against registered mock matchers
        matches = self.matchers.match(request)

        # If not matched, return False
        if not matches:
            return False

        # Increase mock call counter
        self._matches += 1
        if not self._persist:
            self._times -= 1

        # Raise simulated error
        if self._error:
            raise self._error

        # Trigger callback when matched
        for callback in self.callbacks:
            callback(request, self)

        return True

    def __repr__(self):
        """
        Returns an human friendly readable instance data representation.

        Returns:
            str
        """
        keys = ('matches', 'times', 'persist', 'matchers', 'response')

        args = []
        for key in keys:
            if key == 'matchers':
                value = repr(self.matchers).replace('\n  ', '\n    ')
                value = value[:-2] + '  ])'
            elif key == 'response':
                value = repr(self._response)
                value = value[:-1] + '  )'
            else:
                value = repr(getattr(self, '_' + key))
            args.append('{}={}'.format(key, value))

        args = '(\n  {}\n)'.format(',\n  '.join(args))

        return type(self).__name__ + args
