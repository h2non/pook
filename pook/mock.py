import re
from .matchers import *  # noqa
from .decorators import fluent
from .response import Response
# from .request import Request
from .matcher import MatcherEngine
from .helpers import trigger_methods
from .exceptions import PookExpiredMock


class Mock(object):
    """
    Mock represents the HTTP request mock definition
    and expectation DSL.
    """
    def __init__(self,
                 request=None, response=None,
                 **kw):
        self._calls = 0
        self._times = 1
        self._persist = False
        self.request = request
        self.response = response or Response()
        self.matchers = MatcherEngine()
        self.expectations = {}

        # Triggers instance methods based on argument names
        trigger_methods(self, kw)

    @fluent
    def protocol(self, value):
        self.add_matcher(URLProtocolMatcher(value))

    @fluent
    def url(self, url):
        if not url:
            raise Exception('url argument cannot be empty')
        self.add_matcher(URLMatcher(url))

    @fluent
    def method(self, method):
        self.add_matcher(MethodMatcher(method))

    @fluent
    def path(self, path):
        self.add_matcher(PathMatcher(path))

    @fluent
    def header(self, name, value):
        headers = (name, value)
        self.add_matcher(HeadersMatcher(*headers))

    @fluent
    def headers(self, *args):
        self.add_matcher(HeadersMatcher(*args))

    @fluent
    def header_present(self, name):
        headers = {name: re.compile('(.*)')}
        self.add_matcher(HeadersMatcher(headers))

    @fluent
    def headers_present(self, headers):
        headers = {name: re.compile('(.*)') for name in headers}
        self.add_matcher(HeadersMatcher(headers))

    @fluent
    def type(self, value):
        self.add_matcher(HeadersMatcher({'Content-Type': value}))

    @fluent
    def param(self, name, value):
        self.params({name: value})

    @fluent
    def param_exists(self, name):
        self.params({name: '(.*)'})

    @fluent
    def params(self, params):
        self.add_matcher(QueryMatcher(params))

    @fluent
    def json(self, body):
        self.add_matcher(JSONMatcher(body))

    @fluent
    def json_schema(self, schema):
        self.add_matcher(JSONSchemaMatcher(schema))

    @fluent
    def xml(self, body):
        self.add_matcher(XMLMatcher(body))

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

    def reply(self, status=200, **args):
        self.response = Response(status=status, **args)
        return self.response

    def match(self, req):
        if self._times <= 0:
            raise PookExpiredMock('Mock has expired')

        # Match incoming request against registered mock matchers
        matches = self.matchers.match(req)

        # If not matched, return False
        if not matches:
            return False

        # Increase mock call counter
        self._calls += 1
        if not self._persist:
            self._times -= 1

        return True

    def __repr__(self):
        return 'Mock({})'.format(self.matchers)
