import io
import sys
from ..request import Request

# Support Python 2/3
try:
    import mock
except:
    from unittest import mock

if sys.version_info < (3,):     # Python 2
    from httplib import responses as http_reasons
    from cStringIO import StringIO as BytesIO
    from urlparse import urlparse, parse_qsl
else:                           # Python 3
    from http.client import responses as http_reasons
    from io import BytesIO
    from urllib.parse import urlparse, parse_qsl

PATCHES = (
    'requests.packages.urllib3.connectionpool.HTTPConnectionPool.urlopen',
    'urllib3.connectionpool.HTTPConnectionPool.urlopen'
)


def HTTPResponse(*args, **kwargs):
    try:
        from requests.packages.urllib3.response import HTTPResponse
    except:
        from urllib3.response import HTTPResponse
    return HTTPResponse(*args, **kwargs)


def body_io(string, encoding='utf-8'):
    if hasattr(string, 'encode'):
        string = string.encode(encoding)
    return io.BytesIO(string)


class FakeHeaders(list):
    def get_all(self, key, default=None):
        key = key.lower()
        return [v for (k, v) in self if k.lower() == key]
    getheaders = get_all


class FakeResponse(object):
    def __init__(self, headers):
        self.msg = FakeHeaders(headers)

    def isclosed(self):
        return False


class Urllib3Adapter(object):
    def __init__(self, req):
        self.req = req

    def map(self, req):
        req = Request()
        req.url = self.req.url


class Urllib3Interceptor(object):
    """
    urllib3 HTTP traffic interceptor.
    """
    def __init__(self, engine):
        self.patchers = []
        self.engine = engine

    def _on_request(self, pool, method, url,
                    body=None, headers=None, **kwargs):
        req = Request(method)
        req.url = urlparse(pool.scheme + '://' + pool.host + ':' +
                           str(pool.port) + url)
        req.headers = headers
        req.body = body

        print('REQ:', pool, method, url)
        print('URL:', req.url)
        print('HEADERS:', req.headers)
        print('BODY:', body)

        mock = self.engine.on_request(req)
        print('MOCK BODY:', body_io(mock._body).getvalue())

        headers = []
        for key in mock._headers:
            headers.append((key, mock._headers[key]))

        return HTTPResponse(
            body=body_io(mock._body),
            status=mock._status,
            headers=headers,
            preload_content=False,
            reason=http_reasons.get(mock._status),
            original_response=FakeResponse(headers),
        )

    def _patch(self, path):
        def handler(pool, method, url, body=None, headers=None, **kwargs):
            return self._on_request(pool, method, url,
                                    body=body, headers=headers, **kwargs)

        try:
            patcher = mock.patch(path, handler)
            patcher.start()
        except:
            # Exceptions may accur due to missing package
            # Ignore all the exceptions for now
            pass
        else:
            self.patchers.append(patcher)

    def activate(self):
        """
        Activates the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        [self._patch(path) for path in PATCHES]

    def disable(self):
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        [patch.stop() for patch in self.patchers]
