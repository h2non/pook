import asyncio
from http.client import responses as http_reasons
from typing import Callable, Optional
from unittest import mock
from urllib.parse import urlencode, urlunparse
from collections.abc import Mapping

import aiohttp
from aiohttp.helpers import TimerNoop
from aiohttp.streams import EmptyStreamReader

from pook.request import Request  # type: ignore
from pook.interceptors.base import BaseInterceptor

# Try to load yarl URL parser package used by aiohttp
import multidict
import yarl

PATCHES = ("aiohttp.client.ClientSession._request",)

RESPONSE_CLASS = "ClientResponse"
RESPONSE_PATH = "aiohttp.client_reqrep"


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


class AIOHTTPInterceptor(BaseInterceptor):
    """
    aiohttp HTTP client traffic interceptor.
    """

    def _url(self, url) -> Optional[yarl.URL]:
        return yarl.URL(url) if yarl else None

    def set_headers(self, req, headers) -> None:
        # aiohttp's interface allows various mappings, as well as an iterable of key/value tuples
        # ``pook.request`` only allows a dict, so we need to map the iterable to the matchable interface
        if headers:
            if isinstance(headers, Mapping):
                req.headers = headers
            else:
                req_headers: dict[str, str] = {}
                # If it isn't a mapping, then its an Iterable[Tuple[Union[str, istr], str]]
                for req_header, req_header_value in headers:
                    normalised_header = req_header.lower()
                    if normalised_header in req_headers:
                        req_headers[normalised_header] += f", {req_header_value}"
                    else:
                        req_headers[normalised_header] = req_header_value

                req.headers = req_headers

    async def _on_request(
        self,
        _request: Callable,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        data=None,
        headers=None,
        **kw,
    ) -> aiohttp.ClientResponse:
        # Create request contract based on incoming params
        req = Request(method)

        self.set_headers(req, headers)
        self.set_headers(req, session.headers)

        req.body = data

        # Expose extra variadic arguments
        req.extra = kw

        full_url = session._build_url(url)

        # Compose URL
        if not kw.get("params"):
            req.url = str(full_url)
        else:
            req.url = (
                str(full_url)
                + "?"
                + urlencode([(x, y) for x, y in kw["params"].items()])
            )

        # If a json payload is provided, serialize it for JSONMatcher support
        if json_body := kw.get("json"):
            req.json = json_body
            if "Content-Type" not in req.headers:
                req.headers["Content-Type"] = "application/json"

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
        _res = HTTPResponse(session, req.method, self._url(urlunparse(req.url)))

        # response status
        _res.version = aiohttp.HttpVersion(1, 1)
        _res.status = res._status
        _res.reason = http_reasons.get(res._status)

        # Add response headers
        _res._raw_headers = tuple(headers)
        _res._headers = multidict.CIMultiDictProxy(multidict.CIMultiDict(headers))

        if res._body:
            _res.content = SimpleContent(res._body)
        else:
            # Define `_content` attribute with an empty string to
            # force do not read from stream (which won't exists)
            _res.content = EmptyStreamReader()

        # Return response based on mock definition
        return _res

    def _patch(self, path: str) -> None:
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

    def activate(self) -> None:
        """
        Activates the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        for path in PATCHES:
            self._patch(path)

    def disable(self) -> None:
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        for patch in self.patchers:
            patch.stop()
