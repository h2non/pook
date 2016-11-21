import re
from inspect import isfunction, ismethod
from .decorators import fluent
from .response import Response
from .request import Request
from .matcher import MatcherEngine
from .helpers import trigger_methods
from .exceptions import PookExpiredMock
from .matchers import init as matcher  # noqa


def append_funcs(target, items):
    """
    Helper function to append functions into a given list.

    Arguments:
        target (list): receptor list to append functions.
        items (iterable): iterable that yields elements to append.
    """
    [target.append(item) for item in items
     if isfunction(item) or ismethod(item)]


class Mock(object):
    """
    Mock is used to declare and compose the HTTP request/response mock
    definition and matching expectations, which provides fluent API DSL.
    """

    def __init__(self, request=None, response=None, **kw):
        self._calls = 0
        self._times = 1
        self._error = None
        self._persist = False
        self._request = request
        self._response = response or Response()
        self.matchers = MatcherEngine()
        self.filters = []
        self.mappers = []
        self.callbacks = []

        # Triggers instance methods based on argument names
        trigger_methods(self, kw)

        # Trigger request fields
        if request:
            self._trigger_request(request)

    def _trigger_request(self, request):
        if not isinstance(request, Request):
            raise TypeError('request must be instance of pook.Request')

        # Register request matchers
        for key in request.keys:
            if hasattr(self, key):
                getattr(self, key)(getattr(request, key))

    @fluent
    def protocol(self, value):
        self.add_matcher(matcher('URLProtocolMatcher', value))

    @fluent
    def url(self, url):
        self.add_matcher(matcher('URLMatcher', url))

    @fluent
    def method(self, method):
        self.add_matcher(matcher('MethodMatcher', method))

    @fluent
    def path(self, path):
        self.add_matcher(matcher('PathMatcher', path))

    @fluent
    def header(self, name, value):
        headers = (name, value)
        self.add_matcher(matcher('HeadersMatcher', *headers))

    @fluent
    def headers(self, headers=None, **kw):
        headers = kw if kw else headers
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def header_present(self, name):
        headers = {name: re.compile('(.*)')}
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def headers_present(self, headers):
        headers = {name: re.compile('(.*)') for name in headers}
        self.add_matcher(matcher('HeadersMatcher', headers))

    @fluent
    def type(self, value):
        self.content(value)

    @fluent
    def content(self, value):
        self.add_matcher(matcher('HeadersMatcher', {'Content-Type': value}))

    @fluent
    def param(self, name, value):
        self.params({name: value})

    @fluent
    def param_exists(self, name):
        self.params({name: re.compile('(.*)')})

    @fluent
    def params(self, params):
        self.add_matcher(matcher('QueryMatcher', params))

    @fluent
    def json(self, body):
        self.add_matcher(matcher('JSONMatcher', body))

    @fluent
    def json_schema(self, schema):
        self.add_matcher(matcher('JSONSchemaMatcher', schema))

    @fluent
    def xml(self, body):
        self.add_matcher(matcher('XMLMatcher', body))

    @fluent
    def add_matcher(self, matcher):
        self.matchers.add(matcher)

    @fluent
    def use(self, matcher):
        self.add_matcher(matcher)

    @fluent
    def times(self, num=1):
        self._times = num

    @fluent
    def persist(self):
        self._persist = True

    @fluent
    def filter(self, *filters):
        append_funcs(self.filters, filters)

    @fluent
    def map(self, *mappers):
        append_funcs(self.mappers, mappers)

    @fluent
    def callback(self, *callbacks):
        append_funcs(self.callbacks, callbacks)

    @fluent
    def error(self, error):
        """
        Defines a simulated exception error that will be raised.
        """
        self._error = RuntimeError(error) if isinstance(error, str) else error

    def reply(self, status=200, **kw):
        """
        Defines the mock response.

        Returns:
            gook.Response: mock response definition instance.
        """
        res = self._response or Response(**kw)
        res.status = status or res.status
        res.mock = self
        self._response = res
        return res

    def response(self, status=200, **kw):
        """
        Defines the mock response. Alias to ``.reply()``

        Returns:
            gook.Response: mock response definition instance.
        """
        return self.reply(status=status, **kw)

    def isdone(self):
        """
        Returns ``True`` if the mock has been matched by outgoing HTTP traffic.

        Returns:
            bool: ``True`` if the mock was matched succesfully.
        """
        return (self._persist and self._calls > 0) or self._times <= 0

    def match(self, request):
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
        self._calls += 1
        if not self._persist:
            self._times -= 1

        if self._error:
            raise self._error

        # Trigger callback when matched
        for callback in self.callbacks:
            callback(request, self)

        return True

    def __repr__(self):
        keys = ('calls', 'times', 'persist', 'matchers', 'response')

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
