import io
import sys
from ..request import Request
from .base import BaseInterceptor
from .http import URLLIB3_BYPASS

# Support Python 2/3
try:
    import mock
except Exception:
    from unittest import mock

if sys.version_info < (3,):     # Python 2
    from httplib import (
        responses as http_reasons,
        HTTPResponse as ClientHTTPResponse,
    )
else:                           # Python 3
    from http.client import (
        responses as http_reasons,
        HTTPResponse as ClientHTTPResponse,
    )

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


def is_chunked_response(headers):
    tencoding = dict(headers).get("Transfer-Encoding", "").lower()
    return "chunked" in tencoding.split(",")


class MockSock(object):
    @classmethod
    def makefile(cls, *args, **kwargs):
        return


class FakeHeaders(list):
    def get_all(self, key, default=None):
        key = key.lower()
        return [v for (k, v) in self if k.lower() == key]
    getheaders = get_all


class FakeResponse(object):
    def __init__(self, method, headers):
        self._method = method  # name expected by urllib3
        self.msg = FakeHeaders(headers)
        self.closed = False

    def close(self):
        self.closed = True

    def isclosed(self):
        return self.closed


class FakeChunkedResponseBody(object):
    def __init__(self, chunks):
        # append a terminating chunk
        chunks.append(b'')

        self.position = 0
        self.stream = b''.join([self._encode(c) for c in chunks])
        self.closed = False

    def _encode(self, chunk):
        length = '%X\r\n' % len(chunk)
        return length.encode() + chunk + b'\r\n'

    def read_chunk(self, amt=-1, whole=False):
        if whole or amt == -1:
            end_idx = self.stream.index(b'\r\n', self.position) + 2
        else:
            end_idx = self.position + amt

        chunk = self.stream[self.position:end_idx]
        self.position = end_idx

        return chunk

    def readline(self):
        return self.read_chunk(whole=True)

    def read(self, amt=-1):
        return self.read_chunk(amt)

    def flush(self):
        pass

    def close(self):
        self.closed = True


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

        # Shortcut to mock response and response body
        res = mock._response
        body = res._body

        # Aggregate headers as list of tuples for interface compatibility
        headers = []
        for key in res._headers:
            headers.append((key, res._headers[key]))

        if is_chunked_response(headers):
            body_chunks = body if isinstance(body, list) else [body]
            body_chunks = [chunk.encode() for chunk in body_chunks]

            body = ClientHTTPResponse(MockSock)
            body.fp = FakeChunkedResponseBody(body_chunks)
        else:
            # Assume that the body is a bytes-like object
            body = body_io(body)

        # Return mocked HTTP response
        return HTTPResponse(
            path,
            body=body,
            status=res._status,
            headers=headers,
            preload_content=False,
            reason=http_reasons.get(res._status),
            original_response=FakeResponse(method, headers),
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
        except Exception:
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
        patchers_reversed = self.patchers[::-1]
        [patch.stop() for patch in patchers_reversed]
