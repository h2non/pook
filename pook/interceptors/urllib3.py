import io
import sys
from ..request import Request
from .base import BaseInterceptor

# Support Python 2/3
try:
    import mock
except:
    from unittest import mock

if sys.version_info < (3,):     # Python 2
    from httplib import responses as http_reasons
    # from cStringIO import StringIO as BytesIO
    # from urlparse import urlparse
else:                           # Python 3
    from http.client import responses as http_reasons
    # from io import BytesIO
    # from urllib.parse import urlparse

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


class Urllib3Interceptor(BaseInterceptor):
    """
    Urllib3 HTTP traffic interceptor.
    """
    def _on_request(self, pool, method, url,
                    body=None, headers=None, **kwargs):
        # Create request contract based on incoming params
        req = Request(method)
        req.url = '{}://{}:{}{}'.format(
            pool.scheme, pool.host, str(pool.port), url)
        req.headers = headers
        req.body = body

        # Match the request against the registered mocks in pook
        res = self.engine.match(req)

        # Aggregate headers as list of tuples for interface compatibility
        headers = []
        for key in res._headers:
            headers.append((key, res._headers[key]))

        # Return mocked HTTP response
        return HTTPResponse(
            body=body_io(res.body),
            status=res.status,
            headers=headers,
            preload_content=False,
            reason=http_reasons.get(res.status),
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
