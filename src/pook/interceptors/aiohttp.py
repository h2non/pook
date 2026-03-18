from http.client import responses as http_reasons
from typing import Optional
from unittest import mock
from urllib.parse import urlunparse

import aiohttp
from aiohttp.helpers import TimerNoop
from aiohttp.streams import EmptyStreamReader

from pook.request import Request  # type: ignore
from pook.interceptors.base import BaseInterceptor

# Try to load yarl URL parser package used by aiohttp
import multidict
import yarl

RESPONSE_CLASS = "ClientResponse"
RESPONSE_PATH = "aiohttp.client_reqrep"


class AIOHTTPInterceptor(BaseInterceptor):
    # Implements aiohttp.ClientMiddlewareType
    async def __call__(
        self, request: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
    ) -> aiohttp.ClientResponse:
        req = Request(
            method=request.method,
            headers=request.headers.items(),
            body=request.body.decode(),
            url=str(request.url),
        )

        mock = self.engine.match(req)

        # If cannot match any mock, run real HTTP request if networking
        # or silent model are enabled, otherwise this statement won't
        # be reached (an exception will be raised before).
        if not mock:
            return await handler(request)

        # Shortcut to mock response
        res = mock._response

        # Aggregate headers as list of tuples for interface compatibility
        headers = []
        for key in res._headers:
            headers.append((key, res._headers[key]))

        # Create mock equivalent HTTP response
        _res = HTTPResponse(request.session, req.method, self._url(urlunparse(req.url)))

        # response status
        _res.version = aiohttp.HttpVersion(1, 1)
        _res.status = res._status
        _res.reason = http_reasons.get(res._status)

        # Add response headers
        _res._raw_headers = tuple(
            [(bytes(k, "utf-8"), bytes(v, "utf-8")) for k, v in headers]
        )
        _res._headers = multidict.CIMultiDictProxy(multidict.CIMultiDict(headers))

        if res._body:
            _res.content = SimpleContent(res._body)
        else:
            # Define `_content` attribute with an empty string to
            # force do not read from stream (which won't exists)
            _res.content = EmptyStreamReader()

        # Return response based on mock definition
        return _res

    def _url(self, url) -> Optional[yarl.URL]:
        return yarl.URL(url) if yarl else None

    def activate(self) -> None:
        # If not able to import aiohttp dependencies, skip
        if not yarl or not multidict:
            return None

        def _request(session, *args, **kwargs):
            request_middlewares = kwargs.get("middlewares", ())
            kwargs["middlewares"] = request_middlewares + (self,)
            return super_request(session, *args, **kwargs)

        try:
            # Patch ClientSession init to append this interceptor as an aiohttp
            # middleware to all session's middlewares
            patcher = mock.patch("aiohttp.client.ClientSession._request", _request)
            super_request = patcher.get_original()[0]
            # Start patching function calls
            patcher.start()
        except Exception:
            # Exceptions may accur due to missing package
            # Ignore all the exceptions for now
            pass
        else:
            self.patchers.append(patcher)

    def disable(self) -> None:
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        for patch in self.patchers:
            patch.stop()


class SimpleContent(EmptyStreamReader):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content

    async def read(self, n=-1):
        return self.content


def HTTPResponse(session: aiohttp.ClientSession, *args, **kw):
    return session._response_class(
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
