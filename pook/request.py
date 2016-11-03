import sys
from .headers import HTTPHeaderDict
from .helpers import trigger_methods

if sys.version_info < (3,):     # Python 2
    from urlparse import urlparse, parse_qs
else:                           # Python 3
    from urllib.parse import urlparse, parse_qs


class Request(object):
    """
    Request object representing the request mock expectation.
    """
    def __init__(self, method='GET', **args):
        self._url = None
        self._body = None
        self._query = None
        self._method = method
        self._headers = HTTPHeaderDict()
        trigger_methods(self, args)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers.extend(headers)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = urlparse(url)
        self._query = parse_qs(self._url.query)

    @property
    def query(self, url):
        return self._query

    @query.setter
    def query(self, params):
        self._query = parse_qs(params)

    @property
    def body(self, data):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body
