import json
from .decorators import fluent
from .headers import HTTPHeaderDict
from .helpers import trigger_methods

TYPE_ALIASES = {
  'html': 'text/html',
  'json': 'application/json',
  'xml': 'application/xml',
  'urlencoded': 'application/x-www-form-urlencoded',
  'form': 'application/x-www-form-urlencoded',
  'form-data': 'application/x-www-form-urlencoded'
}


class Response(object):
    def __init__(self, **args):
        self._mock = None
        self._body = None
        self._headers = HTTPHeaderDict()
        trigger_methods(self, args)

    @fluent
    def status(self, status=200):
        self._status = status

    @fluent
    def header(self, key, value):
        if type(key) is tuple:
            key, value = str(key[0]), key[1]

        headers = {key: value}
        self._headers.extend(headers)

    @fluent
    def headers(self, headers):
        self._headers.extend(headers)

    @fluent
    def type(self, name):
        value = TYPE_ALIASES.get(name, name)
        self._headers['Content-Type'] = [value]

    @fluent
    def json(self, data):
        self._headers['Content-Type'] = 'application/json'
        self._body = json.dumps(data, indent=4)

    @fluent
    def body(self, body):
        self._body = body

    @property
    def mock(self):
        return self._mock

    @mock.setter
    def mock(self, mock):
        self._mock = mock
