import sys
from .headers import HTTPHeaderDict
from .utils import trigger_methods

if sys.version_info < (3,):     # Python 2
    from urlparse import urlparse
else:                           # Python 3
    from urllib.parse import urlparse


class Request(object):
    """
    Request object representing the request mock expectation.
    """
    def __init__(self, method='GET', **args):
        self._method = method
        self._headers = HTTPHeaderDict()
        self._url = None
        self._body = None
        # Call methods
        trigger_methods(self, args)

    @property
    def method(self):
        return self._method

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        self._headers.extend(headers)

    @property
    def url(self, url):
        return self._url

    @url.setter
    def url(self, url):
        self._url = urlparse(url)
        print('Parsed:', self._url)

    @property
    def body(self, data):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body
