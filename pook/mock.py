import re
import functools
from inspect import isfunction, ismethod
from .decorators import fluent
from .response import Response
from .constants import TYPES
from .request import Request
from .matcher import MatcherEngine
from .helpers import trigger_methods
from .exceptions import PookExpiredMock
from .matchers import init as matcher


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

    Arguments:
        url (str): URL to match.
            E.g: ``server.com/api?foo=bar``.
        method (str): HTTP method name to match.
            E.g: ``GET``.
        path (str): URL path to match.
            E.g: ``/api/users``.
        headers (dict): Header values to match.
            E.g: ``{'server': 'nginx'}``.
        header_present (str): Matches is a header is present.
        headers_present (list|tuple): Matches if multiple headers are present.
        type (str): Matches MIME ``Content-Type`` header.
            E.g: ``json``, ``xml``, ``html``, ``text/plain``
        content (str): Same as ``type`` argument.
        params (dict): Matches the given URL params.
        param_exists (str): Matches if a given URL param exists.
        params_exists (list|tuple): Matches if a given URL params exists.
        body (str|regex): Matches the payload body by regex or
            strict comparison.
        json (dict|list|str|regex): Matches the payload body against the given
            JSON or regular expression.
        jsonschema (dict|str): Matches the payload body against the given
            JSONSchema.
        xml (str|regex): matches the payload body against the given XML string
            or regular expression.
        file (str): Disk file path to load body from. Analog to ``body`` param.
        times (int): Mock TTL or maximum number of times that the mock can be
            matched.
        persist (bool): Enable persistent mode. Mock won't be flushed even if
            it matched one or multiple times.
        delay (int): Optional network delay simulation (only applicable when
            using ``aiohttp`` HTTP client).
        callback (function): optional callback function called every time the
            mock is matched.
        reply (int): Mock response status. Defaults to ``200``.
        response_status (int): Mock response status. Alias to ``reply`` param.
        response_headers (dict): Response headers to use.
        response_type (str): Response MIME type expression or alias.
            Analog to ``type`` param. E.g: ``json``, ``xml``, ``text/plain``.
        response_body (str): Response body to use.
        response_json (dict|list|str): Response JSON to use. If Python is
            passed, it will be serialized as JSON transparently.
        response_xml (str): XML body string to use.
        request (pook.Request): Optional. Request mock definition object.
        response (pook.Response): Optional. Response mock definition
            object.

    Returns:
        pook.Mock
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
        # Optional binded engine where the mock belongs to
        self._engine = None
        # Store request-response mock matched calls
        self._calls = []
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
    def url(self, url):
        """
        Defines the mock URL to match.
        It can be a full URL with path and query params.

        Protocol schema is optional, defaults to ``http://``.

        Arguments:
            url (str): mock URL to match. E.g: ``server.com/api``.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('URLMatcher', url))

    @fluent
    def method(self, method):
        """
        Defines the HTTP method to match.
        Use ``*`` to match any method.

        Arguments:
            method (str): method value to match. E.g: ``GET``.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('MethodMatcher', method))

    @fluent
    def path(self, path):
        """
        Defines a URL path to match.

        Only call this method if the URL has no path already defined.

        Arguments:
            path (str): URL path value to match. E.g: ``/api/users``.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('PathMatcher', path))

    @fluent
    def header(self, name, value):
        """
        Defines a URL path to match.

        Only call this method if the URL has no path already defined.

        Arguments:
            path (str): URL path value to match. E.g: ``/api/users``.

        Returns:
            self: current Mock instance.
        """
        headers = {name: value}
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def headers(self, headers=None, **kw):
        """
        Defines a dictionary of arguments.

        Header keys are case insensitive.

        Arguments:
            headers (dict): headers to match.
            **headers (dict): headers to match as variadic keyword arguments.

        Returns:
            self: current Mock instance.
        """
        headers = kw if kw else headers
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def header_present(self, *names):
        """
        Defines a new header matcher expectation that must be present in the
        outgoing request in order to be satisfied, no matter what value it
        hosts.

        Header keys are case insensitive.

        Arguments:
            *names (str): header or headers names to match.

        Returns:
            self: current Mock instance.

        Example::

            (pook.get('server.com/api')
                .header_present('content-type'))
        """
        for name in names:
            headers = {name: re.compile('(.*)')}
            self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def headers_present(self, headers):
        """
        Defines a list of headers that must be present in the
        outgoing request in order to satisfy the matcher, no matter what value
        the headers hosts.

        Header keys are case insensitive.

        Arguments:
            headers (list|tuple): header keys to match.

        Returns:
            self: current Mock instance.

        Example::

            (pook.get('server.com/api')
                .headers_present(['content-type', 'Authorization']))
        """
        headers = {name: re.compile('(.*)') for name in headers}
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def type(self, value):
        """
        Defines the request ``Content-Type`` header to match.

        You can pass one of the following aliases instead of the full
        MIME type representation:

        - ``json`` = ``application/json``
        - ``xml`` = ``application/xml``
        - ``html`` = ``text/html``
        - ``text`` = ``text/plain``
        - ``urlencoded`` = ``application/x-www-form-urlencoded``
        - ``form`` = ``application/x-www-form-urlencoded``
        - ``form-data`` = ``application/x-www-form-urlencoded``

        Arguments:
            value (str): type alias or header value to match.

        Returns:
            self: current Mock instance.
        """
        self.content(value)

    @fluent
    def content(self, value):
        """
        Defines the ``Content-Type`` outgoing header value to match.

        You can pass one of the following type aliases instead of the full
        MIME type representation:

        - ``json`` = ``application/json``
        - ``xml`` = ``application/xml``
        - ``html`` = ``text/html``
        - ``text`` = ``text/plain``
        - ``urlencoded`` = ``application/x-www-form-urlencoded``
        - ``form`` = ``application/x-www-form-urlencoded``
        - ``form-data`` = ``application/x-www-form-urlencoded``

        Arguments:
            value (str): type alias or header value to match.

        Returns:
            self: current Mock instance.
        """
        header = {'Content-Type': TYPES.get(value, value)}
        self.add_matcher(matcher('HeadersMatcher', header))

    @fluent
    def param(self, name, value):
        """
        Defines an URL param key and value to match.

        Arguments:
            name (str): param name value to match.
            value (str): param name value to match.

        Returns:
            self: current Mock instance.
        """
        self.params({name: value})

    @fluent
    def param_exists(self, name):
        """
        Checks if a given URL param name is present in the URL.

        Arguments:
            name (str): param name to check existence.

        Returns:
            self: current Mock instance.
        """
        self.params({name: re.compile('(.*)')})

    @fluent
    def params(self, params):
        """
        Defines a set of URL query params to match.

        Arguments:
            params (dict): set of params to match.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('QueryMatcher', params))

    @fluent
    def body(self, body):
        """
        Defines the body data to match.

        ``body`` argument can be a ``str``, ``binary`` or a regular expression.

        Arguments:
            body (str|binary|regex): body data to match.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('BodyMatcher', body))

    @fluent
    def json(self, json):
        """
        Defines the JSON body to match.

        ``json`` argument can be an JSON string, a JSON serializable
        Python structure, such as a ``dict`` or ``list`` or it can be
        a regular expression used to match the body.

        Arguments:
            json (str|dict|list|regex): body JSON to match.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('JSONMatcher', json))

    @fluent
    def jsonschema(self, schema):
        """
        Defines a JSONSchema representation to be used for body matching.

        Arguments:
            schema (str|dict): dict or JSONSchema string to use.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('JSONSchemaMatcher', schema))

    @fluent
    def xml(self, xml):
        """
        Defines a XML body value to match.

        Arguments:
            xml (str|regex): body XML to match.

        Returns:
            self: current Mock instance.
        """
        self.add_matcher(matcher('XMLMatcher', xml))

    @fluent
    def file(self, path):
        """
        Reads the body to match from a disk file.

        Arguments:
            path (str): relative or absolute path to file to read from.

        Returns:
            self: current Mock instance.
        """
        with open(path, 'r') as f:
            self.body(str(f.read()))

    @fluent
    def add_matcher(self, matcher):
        """
        Adds one or multiple custom matchers instances.

        Matchers must implement the following interface:

        - ``.__init__(expectation)``
        - ``.match(request)``
        - ``.name = str``

        Matchers can optionally inherit from ``pook.matchers.BaseMatcher``.

        Arguments:
            *matchers (pook.matchers.BaseMatcher): matchers to add.

        Returns:
            self: current Mock instance.
        """
        self.matchers.add(matcher)

    @fluent
    def use(self, *matchers):
        """
        Adds one or multiple custom matchers instances.

        Matchers must implement the following interface:

        - ``.__init__(expectation)``
        - ``.match(request)``
        - ``.name = str``

        Matchers can optionally inherit from ``pook.matchers.BaseMatcher``.

        Arguments:
            *matchers (pook.matchers.BaseMatcher): matchers to add.

        Returns:
            self: current Mock instance.
        """
        [self.add_matcher(matcher) for matcher in matchers]

    @fluent
    def times(self, times=1):
        """
        Defines the TTL limit for the current mock.

        The TTL number will determine the maximum number of times that the
        current mock can be matched and therefore consumed.

        Arguments:
            times (int): TTL number. Defaults to ``1``.

        Returns:
            self: current Mock instance.
        """
        self._times = times

    @fluent
    def persist(self):
        """
        Enables persistent mode for the current mock.

        Returns:
            self: current Mock instance.
        """
        self._persist = True

    @fluent
    def filter(self, *filters):
        """
        Registers one o multiple request filters used during the matching
        phase.

        Arguments:
            *mappers (function): variadic mapper functions.

        Returns:
            self: current Mock instance.
        """
        _append_funcs(self.filters, filters)

    @fluent
    def map(self, *mappers):
        """
        Registers one o multiple request mappers used during the mapping
        phase.

        Arguments:
            *mappers (function): variadic mapper functions.

        Returns:
            self: current Mock instance.
        """
        _append_funcs(self.mappers, mappers)

    @fluent
    def callback(self, *callbacks):
        """
        Registers one or multiple callback that will be called every time the
        current mock matches an outgoing HTTP request.

        Arguments:
            *callbacks (function): callback functions to call.

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

        Arguments:
            error (str|Exception): error to raise.

        Returns:
            self: current Mock instance.
        """
        self._error = RuntimeError(error) if isinstance(error, str) else error

    def reply(self, status=200, **kw):
        """
        Defines the mock response.

        Arguments:
            status (int, optional): response status code. Defaults to ``200``.
            **kw (dict): optional keyword arguments passed to ``pook.Response``
                constructor.

        Returns:
            pook.Response: mock response definition instance.
        """
        # Use or create a Response mock instance
        res = self._response or Response(**kw)
        # Define HTTP mandatory response status
        res.status(status or res._status)
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

        Arguments:
            status (int): response status code. Defaults to ``200``.
            **kw (dict): optional keyword arguments passed to ``pook.Response``
                constructor.

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

    def ismatched(self):
        """
        Returns ``True`` is the mock has been matched at least once time.

        Returns:
            bool
        """
        return self._matches > 0

    @property
    def done(self):
        """
        Attribute accessor that would be ``True`` if the current mock
        is done, and therefore have been matched multiple times.

        Returns:
            bool
        """
        return self.isdone()

    @property
    def matched(self):
        """
        Accessor property that would be ``True`` if the current mock
        have been matched at least once.

        See ``Mock.total_matches`` for more information.

        Returns:
            bool
        """
        return self._matches > 0

    @property
    def total_matches(self):
        """
        Accessor property to retrieve the total number of times that the
        current mock has been matched.

        Returns:
            int
        """
        return self._matches

    @property
    def matches(self):
        """
        Accessor to retrieve the mock match calls registry.

        Returns:
            list[MockCall]
        """
        return self._calls

    @property
    def calls(self):
        """
        Accessor to retrieve the mock match calls registry.

        Returns:
            list[MockCall]
        """
        return self.matches

    def match(self, request):
        """
        Matches an outgoing HTTP request against the current mock matchers.

        This method acts like a delegator to `pook.MatcherEngine`.

        Arguments:
            request (pook.Request): request instance to match.

        Raises:
            Exception: if the mock has an exception defined.

        Returns:
            tuple(bool, list[Exception]): ``True`` if the mock matches
                the outgoing HTTP request, otherwise ``False``. Also returns
                an optional list of error exceptions.
        """
        # If mock already expired, fail it
        if self._times <= 0:
            raise PookExpiredMock('Mock expired')

        # Trigger mock filters
        for test in self.filters:
            if not test(request, self):
                return False, []

        # Trigger mock mappers
        for mapper in self.mappers:
            request = mapper(request, self)
            if not request:
                raise ValueError('map function must return a request object')

        # Match incoming request against registered mock matchers
        matches, errors = self.matchers.match(request)

        # If not matched, return False
        if not matches:
            return False, errors

        # Register matched request for further inspecion and reference
        self._calls.append(request)

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

        return True, []

    def __call__(self, fn):
        """
        Overload Mock instance as callable object in order to be used
        as decorator definition syntax.

        Arguments:
            fn (function): function to decorate.

        Returns:
            function or pook.Mock
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
        def decorator(*args, **kw):
            # Force engine activation, if available
            # This prevents state issue while declaring mocks as decorators.
            # This might be removed in the future.
            if self._engine:
                self._engine.activate()

            # Call decorated target function
            return fn(*args, **kw)

        return decorator

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
