from ..request import Request
from .base import BaseInterceptor

# Support Python 2/3
try:
    import mock
except Exception:
    from unittest import mock


class MockFrame(object):
    def __init__(self, opcode, data, fin=1):
        self.opcode = opcode
        self.data = data
        self.fin = fin


class MockSocket(object):
    def fileno(self):
        return 0

    def gettimeout(self):
        return 0


class MockHandshakeResponse(object):

    def __init__(self, status, headers, subprotocol):
        self.status = status
        self.headers = headers
        self.subprotocol = subprotocol


class WebSocketInterceptor(BaseInterceptor):

    def _handshake(self, sock, hostname, port, resource, **options):
        return MockHandshakeResponse(200, {}, "")

    def _connect(self, url, options, proxy, socket):
        req = Request()
        req.headers = {}  # TODO
        req.url = url

        # TODO does this work multithreaded?!?
        self._mock = self.engine.match(req)
        if not self._mock:
            # we cannot forward, as we have mocked away the connection
            raise ValueError(
                "Request to '%s' could not be matched or forwarded" % url
            )

        # make the body always a list to simplify our lives
        body = self._mock._response._body
        if not isinstance(body, list):
            self._mock._response._body = [body]

        sock = MockSocket()
        addr = ("hostname", "port", "resource")

        return sock, addr

    def _send(self, data):
        # mock as if all data has been sent
        return len(data)

    def _recv_frame(self):
        # alias
        body = self._mock._response._body

        idx = getattr(self, "_data_index", 0)
        if len(body) <= idx:
            # close frame
            return MockFrame(0x8, None)

        # data frame
        self._data_index = idx + 1
        return MockFrame(0x1, body[idx].encode("utf-8"), 1)

    def _patch(self, path, handler):
        try:
            # Create a new patcher for Urllib3 urlopen function
            # used as entry point for all the HTTP communications
            patcher = mock.patch(path, handler)
            # Retrieve original patched function that we might need for real
            # networking
            # request = patcher.get_original()[0]
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
        patches = [
            ('websocket._core.connect', self._connect),
            ('websocket._core.handshake', self._handshake),
            ('websocket.WebSocket._send', self._send),
            ('websocket.WebSocket.recv_frame', self._recv_frame),
        ]

        [self._patch(path, handler) for path, handler in patches]

    def disable(self):
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        [patch.stop() for patch in self.patchers]
