from ..request import Request
from .base import BaseInterceptor

from unittest import mock

from urllib.parse import urlunparse, urlencode
from http.client import responses as http_reasons

import asyncio
from aiohttp.helpers import TimerNoop
from aiohttp.streams import EmptyStreamReader

# Try to load yarl URL parser package used by aiohttp
try:
    import yarl
    import multidict
except Exception:
    yarl, multidict = None, None

PATCHES = ("aiohttp.client.ClientSession._request",)

RESPONSE_CLASS = "ClientResponse"
RESPONSE_PATH = "aiohttp.client_reqrep"


class SimpleContent(EmptyStreamReader):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content

    async def read(self, n=-1):
        return self.content


def HTTPResponse(*args, **kw):
    # Dynamically load package
    module = __import__(RESPONSE_PATH, fromlist=(RESPONSE_CLASS,))
    ClientResponse = getattr(module, RESPONSE_CLASS)

    # Return response instance
    return ClientResponse(
        *args,
        request_info=mock.Mock(),
        writer=None,
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=mock.Mock(),
        session=mock.Mock(),
        **kw,
    )


class AIOHTTPInterceptor(BaseInterceptor):
    """
    aiohttp HTTP client traffic interceptor.
    """

    def _url(self, url):
        return yarl.URL(url) if yarl else None

    async def _on_request(
        self, _request, session, method, url, data=None, headers=None, **kw
    ):
        # Create request contract based on incoming params
        req = Request(method)
        req.headers = headers or {}
        req.body = data

        # Expose extra variadic arguments
        req.extra = kw

        # Compose URL
        if not kw.get("params"):
            req.url = str(url)
        else:
            req.url = (
                str(url) + "?" + urlencode([(x, y) for x, y in kw["params"].items()])
            )

        # Match the request against the registered mocks in pook
        mock = self.engine.match(req)

        # If cannot match any mock, run real HTTP request if networking
        # or silent model are enabled, otherwise this statement won't
        # be reached (an exception will be raised before).
        if not mock:
            return await _request(
                session, method, url, data=data, headers=headers, **kw
            )

        # Simulate network delay
        if mock._delay:
            await asyncio.sleep(mock._delay / 1000)  # noqa

        # Shortcut to mock response
        res = mock._response

        # Aggregate headers as list of tuples for interface compatibility
        headers = []
        for key in res._headers:
            headers.append((key, res._headers[key]))

        # Create mock equivalent HTTP response
        _res = HTTPResponse(req.method, self._url(urlunparse(req.url)))

        # response status
        _res.version = (1, 1)
        _res.status = res._status
        _res.reason = http_reasons.get(res._status)
        _res._should_close = False

        # Add response headers
        _res._raw_headers = tuple(headers)
        _res._headers = multidict.CIMultiDictProxy(multidict.CIMultiDict(headers))

        if res._body:
            _res.content = SimpleContent(
                res._body
                if res._binary
                else res._body.encode("utf-8", errors="replace"),
            )
        else:
            # Define `_content` attribute with an empty string to
            # force do not read from stream (which won't exists)
            _res.content = EmptyStreamReader()

        # Return response based on mock definition
        return _res

    def _patch(self, path):
        # If not able to import aiohttp dependencies, skip
        if not yarl or not multidict:
            return None

        async def handler(session, method, url, data=None, headers=None, **kw):
            return await self._on_request(
                _request, session, method, url, data=data, headers=headers, **kw
            )

        try:
            # Create a new patcher for Urllib3 urlopen function
            # used as entry point for all the HTTP communications
            patcher = mock.patch(path, handler)
            # Retrieve original patched function that we might need for real
            # networking
            _request = patcher.get_original()[0]
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
        [patch.stop() for patch in self.patchers]
