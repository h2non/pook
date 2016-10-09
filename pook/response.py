import json
from .headers import HTTPHeaderDict

TYPE_ALIASES = {
  'html': 'text/html',
  'json': 'application/json',
  'xml': 'application/xml',
  'urlencoded': 'application/x-www-form-urlencoded',
  'form': 'application/x-www-form-urlencoded',
  'form-data': 'application/x-www-form-urlencoded'
}


class Response(object):
    def __init__(self, status=200):
        self._body = None
        self._status = status
        self._headers = HTTPHeaderDict()

    def status(seld, status=200):
        self._status = status

    def headers(self, headers):
        self._headers.extend(headers)

    def type(self, name):
        value = TYPE_ALIASES.get(name, name)
        self._headers['Content-Type'] = [value]

    def json(self, data):
        self._headers['Content-Type'] = 'application/json'
        self._body = json.dumps(data)

    def body(self, body):
        self._body = body
