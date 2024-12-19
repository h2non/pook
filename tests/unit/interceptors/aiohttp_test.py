import aiohttp
import pytest

import pook
from tests.unit.fixtures import BINARY_FILE
from tests.unit.interceptors.base import StandardTests

pytestmark = [pytest.mark.pook]


class TestStandardAiohttp(StandardTests):
    is_async = True

    async def amake_request(self, method, url, content=None, headers=None):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            response = await session.request(
                method=method, url=url, data=content, headers=headers
            )
            response_content = await response.read()
            return response.status, response_content, response.headers


def _pook_url(url):
    return pook.head(url).reply(200).mock


@pytest.mark.asyncio
async def test_async_with_request(url_404):
    mock = _pook_url(url_404)
    async with aiohttp.ClientSession() as session:
        async with session.head(url_404) as req:
            assert req.status == 200

    assert len(mock.matches) == 1


@pytest.mark.asyncio
async def test_await_request(url_404):
    mock = _pook_url(url_404)
    async with aiohttp.ClientSession() as session:
        req = await session.head(url_404)
        assert req.status == 200

    assert len(mock.matches) == 1


@pytest.mark.asyncio
async def test_binary_body(url_404):
    pook.get(url_404).reply(200).body(BINARY_FILE)
    async with aiohttp.ClientSession() as session:
        req = await session.get(url_404)
        assert await req.read() == BINARY_FILE


@pytest.mark.asyncio
async def test_json_matcher_json_payload(url_404):
    payload = {"foo": "bar"}
    pook.post(url_404).json(payload).reply(200).body(BINARY_FILE)
    async with aiohttp.ClientSession() as session:
        req = await session.post(url_404, json=payload)
        assert await req.read() == BINARY_FILE


@pytest.mark.asyncio
async def test_client_base_url(local_responder):
    """Client base url should be matched."""
    pook.get(local_responder + "/status/404").reply(200).body("hello from pook")
    async with aiohttp.ClientSession(base_url=local_responder.url) as session:
        res = await session.get("/status/404")
        assert res.status == 200
        assert await res.read() == b"hello from pook"


@pytest.mark.asyncio
async def test_client_headers(local_responder):
    """Headers set on the client should be matched."""
    pook.get(local_responder + "/status/404").header("x-pook", "hello").reply(200).body(
        "hello from pook"
    )
    async with aiohttp.ClientSession(headers={"x-pook": "hello"}) as session:
        res = await session.get(local_responder + "/status/404")
        assert res.status == 200
        assert await res.read() == b"hello from pook"


@pytest.mark.asyncio
async def test_client_headers_merged(local_responder):
    """Headers set on the client should be matched even if request-specific headers are sent."""
    pook.get(local_responder + "/status/404").header("x-pook", "hello").reply(200).body(
        "hello from pook"
    )
    async with aiohttp.ClientSession(headers={"x-pook": "hello"}) as session:
        res = await session.get(
            local_responder + "/status/404", headers={"x-pook-secondary": "xyz"}
        )
        assert res.status == 200
        assert await res.read() == b"hello from pook"


@pytest.mark.asyncio
async def test_client_headers_both_session_and_request(local_responder):
    """Headers should be matchable from both the session and request in the same matcher"""
    pook.get(local_responder + "/status/404").header("x-pook-session", "hello").header(
        "x-pook-request", "hey"
    ).reply(200).body("hello from pook")
    async with aiohttp.ClientSession(headers={"x-pook-session": "hello"}) as session:
        res = await session.get(
            local_responder + "/status/404", headers={"x-pook-request": "hey"}
        )
        assert res.status == 200
        assert await res.read() == b"hello from pook"
