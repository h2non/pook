import io
import sys
from ..request import Request
from .base import BaseInterceptor
from .http import URLLIB3_BYPASS

# Support Python 2/3
try:
    import mock
except:
    from unittest import mock

if sys.version_info < (3,):     # Python 2
    from httplib import responses as http_reasons
else:                           # Python 3
    from http.client import responses as http_reasons

PATCHES = (
    'requests.packages.urllib3.connectionpool.HTTPConnectionPool.urlopen',
    'urllib3.connectionpool.HTTPConnectionPool.urlopen'
)

RESPONSE_CLASS = 'HTTPResponse'

RESPONSE_PATH = {
    'requests': 'requests.packages.urllib3.response',
    'urllib3': 'urllib3.response'
}


def HTTPResponse(path, *args, **kw):
    # Infer package
    package = path.split('.').pop(0)
    # Get import path
    import_path = RESPONSE_PATH.get(package)

    # Dynamically load package
    module = __import__(import_path, fromlist=(RESPONSE_CLASS,))
    HTTPResponse = getattr(module, RESPONSE_CLASS)

    # Return response instance
    return HTTPResponse(*args, **kw)


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


class Urllib3Interceptor(BaseInterceptor):
    """
    Urllib3 HTTP traffic interceptor.
    """

    def _on_request(self, urlopen, path, pool, method, url,
                    body=None, headers=None, **kw):
        # Remove bypass headers
        real_headers = dict(headers or {})
        real_headers.pop(URLLIB3_BYPASS)

        # Create request contract based on incoming params
        req = Request(method)
        req.headers = real_headers
        req.body = body

        # Compose URL
        req.url = '{}://{}:{:d}{}'.format(
            pool.scheme,
            pool.host,
            pool.port or 80,
            url
        )

        # Match the request against the registered mocks in pook
        mock = self.engine.match(req)

        # If cannot match any mock, run real HTTP request since networking
        # or silent model will be enabled, otherwise this statement won't
        # be reached (an exception will be raised before).
        if not mock:
            return urlopen(pool, method, url, body=body, headers=headers, **kw)

        # Shortcut to mock response
        res = mock._response

        # Aggregate headers as list of tuples for interface compatibility
        headers = []
        for key in res._headers:
            headers.append((key, res._headers[key]))

        # Return mocked HTTP response
        return HTTPResponse(
            path,
            body=body_io(res._body),
            status=res._status,
            headers=headers,
            preload_content=False,
            reason=http_reasons.get(res._status),
            original_response=FakeResponse(headers),
        )

    def _patch(self, path):
        def handler(conn, method, url, body=None, headers=None, **kw):
            # Flag that the current request as urllib3 intercepted
            headers = headers or {}
            headers[URLLIB3_BYPASS] = True

            # Call request interceptor
            return self._on_request(urlopen, path, conn, method, url,
                                    body=body, headers=headers, **kw)

        try:
            # Create a new patcher for Urllib3 urlopen function
            # used as entry point for all the HTTP communications
            patcher = mock.patch(path, handler)
            # Retrieve original patched function that we might need for real
            # networking
            urlopen = patcher.get_original()[0]
            # Start patching function calls
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
