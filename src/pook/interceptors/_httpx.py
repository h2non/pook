from ..request import Request
from .base import BaseInterceptor

from http.client import responses as http_reasons

from unittest import mock
import asyncio

import httpx

PATCHES = (
    "httpx.Client._transport_for_url",
    "httpx.AsyncClient._transport_for_url",
)


class HttpxInterceptor(BaseInterceptor):
    """
    httpx client traffic interceptor.

    Intercepts synchronous and asynchronous httpx traffic.
    """

    def _patch(self, path):
        if "AsyncClient" in path:
            transport_cls = AsyncTransport
        else:
            transport_cls = SyncTransport

        def handler(client, *_):
            return transport_cls(self, client, _original_transport_for_url)

        try:
            patcher = mock.patch(path, handler)
            _original_transport_for_url = patcher.get_original()[0]
            patcher.start()
        except Exception:
            pass
        else:
            self.patchers.append(patcher)

    def activate(self):
        [self._patch(path) for path in PATCHES]

    def deactivate(self):
        [patch.stop() for patch in self.patchers]


class MockedTransport(httpx.BaseTransport):
    def __init__(self, interceptor, client, _original_transport_for_url):
        self._interceptor = interceptor
        self._client = client
        self._original_transport_for_url = _original_transport_for_url

    def _get_pook_request(self, httpx_request):
        req = Request(httpx_request.method)
        req.url = str(httpx_request.url)
        req.headers = httpx_request.headers

        return req

    def _get_httpx_response(self, httpx_request, mock_response):
        res = httpx.Response(
            status_code=mock_response._status,
            headers=mock_response._headers,
            content=mock_response._body,
            extensions={
                # TODO: Add HTTP2 response support
                "http_version": b"HTTP/1.1",
                "reason_phrase": http_reasons.get(mock_response._status).encode(
                    "ascii"
                ),
                "network_stream": None,
            },
            request=httpx_request,
        )

        # Allow to read the response on client side
        res.is_stream_consumed = False
        res.is_closed = False
        if hasattr(res, "_content"):
            del res._content

        return res


class AsyncTransport(MockedTransport):
    async def _get_pook_request(self, httpx_request):
        req = super()._get_pook_request(httpx_request)
        req.body = await httpx_request.aread()
        return req

    async def handle_async_request(self, request):
        pook_request = await self._get_pook_request(request)

        mock = self._interceptor.engine.match(pook_request)

        if not mock:
            transport = self._original_transport_for_url(self._client, self.request.url)
            return await transport.handle_async_request(request)

        if mock._delay:
            await asyncio.sleep(mock._delay / 1000)

        return self._get_httpx_response(request, mock._response)


class SyncTransport(MockedTransport):
    def _get_pook_request(self, httpx_request):
        req = super()._get_pook_request(httpx_request)
        req.body = httpx_request.read()
        return req

    def handle_request(self, request):
        pook_request = self._get_pook_request(request)

        mock = self._interceptor.engine.match(pook_request)

        if not mock:
            transport = self._original_transport_for_url(self._client, request.url)
            return transport.handle_request(request)

        return self._get_httpx_response(request, mock._response)
