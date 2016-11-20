import json
from .decorators import fluent
from .headers import HTTPHeaderDict
from .helpers import trigger_methods

TYPES = {
  'html': 'text/html',
  'json': 'application/json',
  'xml': 'application/xml',
  'urlencoded': 'application/x-www-form-urlencoded',
  'form': 'application/x-www-form-urlencoded',
  'form-data': 'application/x-www-form-urlencoded'
}


class Response(object):
    """
    Response is used to declare and compose an HTTP mock response.
    Provides a chainable DSL.
    """

    def __init__(self, **args):
        self._status = 200
        self._mock = None
        self._body = None
        self._headers = HTTPHeaderDict()

        # Trigger response method based on input arguments
        trigger_methods(self, args)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = int(status)

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
    def set(self, header, value):
        self._headers[header] = value

    @fluent
    def type(self, name):
        self.content(name)

    @fluent
    def content(self, name):
        self._headers['Content-Type'] = TYPES.get(name, name)

    @fluent
    def json(self, data):
        self._headers['Content-Type'] = 'application/json'
        print('>>> data:', data)
        self._body = json.dumps(data, indent=4)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def mock(self):
        return self._mock

    @mock.setter
    def mock(self, mock):
        self._mock = mock

    def __repr__(self):
        args = []
        for key in ('headers', 'status', 'body'):
            value = getattr(self, '_{}'.format(key))
            args.append('{}={}'.format(key, value))
        return 'Response(\n    {}\n)'.format(',\n    '.join(args))
