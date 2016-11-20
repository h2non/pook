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

    # Store keys
    keys = ('method', 'headers', 'body', 'url', 'query')

    def __init__(self, method='GET', **kw):
        self._url = None
        self._body = None
        self._query = None
        self._method = method
        self._extra = kw.get('extra')
        self._headers = HTTPHeaderDict()

        trigger_methods(self, kw)

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
        if not hasattr(headers, '__setitem__'):
            raise TypeError('headers must be a dictionary')
        self._headers.extend(headers)

    @property
    def extra(self):
        return self._extra

    @extra.setter
    def extra(self, extra):
        if not isinstance(extra, dict):
            raise TypeError('extra must be a dictionary')
        self._extra = extra

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
        if hasattr(body, 'decode'):
            try:
                body = body.decode('utf-8', 'strict')
            except:
                pass

        self._body = body

    def copy(self):
        req = type(self)()
        req.__dict__ = self.__dict__.copy()
        req._headers = self.headers.copy()
        return req

    def __repr__(self):
        args = []
        for key in self.keys:
            value = getattr(self, '_{}'.format(key))
            args.append('{}={},\n'.format(key, value))
        return 'Request(\n  {})'.format('  '.join(args))
