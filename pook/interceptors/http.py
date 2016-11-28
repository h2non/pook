import sys
import socket
from ..request import Request
from .base import BaseInterceptor

# Support Python 2/3
try:
    import mock
except:
    from unittest import mock

if sys.version_info < (3,):     # Python 2
    from httplib import responses as http_reasons, _CS_REQ_SENT
else:                           # Python 3
    from http.client import responses as http_reasons, _CS_REQ_SENT

PATCHES = (
    'http.client.HTTPConnection.request',
)

RESPONSE_CLASS = 'HTTPResponse'
RESPONSE_PATH = 'http.client'

URLLIB3_BYPASS = '__urllib3_bypass__'


def HTTPResponse(*args, **kw):
    # Dynamically load package
    module = __import__(RESPONSE_PATH, fromlist=(RESPONSE_CLASS,))
    HTTPResponse = getattr(module, RESPONSE_CLASS)

    # Return response instance
    return HTTPResponse(*args, **kw)


class SocketMock(socket.socket):
    def __init__(self):
        pass

    def makefile(self, *args, **kw):
        pass

    def close(self, *args, **kw):
        pass


class HTTPClientInterceptor(BaseInterceptor):
    """
    urllib / http.client HTTP traffic interceptor.
    """

    def _on_request(self, _request, conn, method, url,
                    body=None, headers=None, **kw):
        # Create request contract based on incoming params
        req = Request(method)
        req.headers = headers or {}
        req.body = body

        # Compose URL
        req.url = 'http://{}:{}{}'.format(conn.host, conn.port, url)

        # Match the request against the registered mocks in pook
        mock = self.engine.match(req)

        # If cannot match any mock, run real HTTP request since networking,
        # otherwise this statement won't be reached
        # (an exception will be raised before).
        if not mock:
            return _request(conn, method, url,
                            body=body, headers=headers, **kw)

        # Shortcut to mock response
        res = mock._response

        # Aggregate headers as list of tuples for interface compatibility
        headers = []
        for key in res._headers:
            headers.append((key, res._headers[key]))

        mockres = HTTPResponse(SocketMock(), method=method, url=url)
        mockres.version = (1, 1)
        mockres.status = res._status
        mockres.reason = http_reasons.get(res._status)
        mockres.headers = res._headers.to_dict()

        def getresponse():
            return mockres
        conn.getresponse = getresponse

        conn.__response = mockres
        conn.__state = _CS_REQ_SENT

        # Path reader
        def read():
            return res._body or ''
        mockres.read = read

        return mockres

    def _patch(self, path):
        def handler(conn, method, url, body=None, headers=None, **kw):
            # Detect if httplib was called by urllib3 interceptor
            # This is a bit ugly, I know. Ideas are welcome!
            if headers and URLLIB3_BYPASS in headers:
                # Remove bypass header used as flag
                headers.pop(URLLIB3_BYPASS)
                # Call original patched function
                return request(conn, method, url,
                               body=body, headers=headers, **kw)

            # Otherwise call the request interceptor
            return self._on_request(request, conn, method, url,
                                    body=body, headers=headers, **kw)

        try:
            # Create a new patcher for Urllib3 urlopen function
            # used as entry point for all the HTTP communications
            patcher = mock.patch(path, handler)
            # Retrieve original patched function that we might need for real
            # networking
            request = patcher.get_original()[0]
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
