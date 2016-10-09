import re
from .matchers import *  # noqa
from .decorators import fluent
from .response import Response
from .request import Request
from .matcher import MatcherEngine
from .exceptions import PockExpiredMock


# class CallList(Sequence, Sized):
#     def __init__(self):
#         self._calls = []

#     def __iter__(self):
#         return iter(self._calls)

#     def __len__(self):
#         return len(self._calls)

#     def __getitem__(self, idx):
#         return self._calls[idx]

#     def add(self, request, response):
#         self._calls.append(Call(request, response))

#     def reset(self):
#         self._calls = []


class Mock(object):
    """
    Mock represents the HTTP request mock definition
    and expectation DSL.
    """
    def __init__(self, url,
                 path='',
                 method='GET',
                 params=None,
                 headers=None,
                 body=None):
        self._calls = 0
        self._times = 1
        self._persist = False
        self.request = Request()
        self.response = Response()
        self.matchers = MatcherEngine()
        self.method(method)
        self.url(url)
        self.params = {}
        self.body = body
        # self.args = kwargs

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
        headers = (name, re.compile('(.*)'))
        self.add_matcher(HeadersMatcher(*headers))

    @fluent
    def headers_present(self, name):
        headers

    @fluent
    def type(self, value):
        self.add_matcher(HeadersMatcher(('Content-Type', value)))

    @fluent
    def query_param(self, name, value):
        query = (name, value)
        self.add_matcher(QueryMatcher(query))

    @fluent
    def query_exists(self, name):
        query = (name, '(.*)')
        self.add_matcher(QueryMatcher(query))

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

    def reply(self, status=200):
        self.response._status = status
        return self.response

    def match(self, req):
        if self._times <= 0:
            raise PockExpiredMock('Mock has expired')

        # Match incoming request against registered mock matchers
        matches = self.matchers.match(req)

        # If not matched, return False
        if not matches:
            return False

        # Increase mock counters
        self._calls += 1
        if not self._persist:
            self._times -= 1

        return True
