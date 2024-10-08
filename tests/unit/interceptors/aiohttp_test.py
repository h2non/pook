import json

import aiohttp
import pytest

import pook
from tests.unit.fixtures import BINARY_FILE
from tests.unit.interceptors.base import StandardTests

pytestmark = [pytest.mark.pook]


class TestStandardAiohttp(StandardTests):
    is_async = True

    async def amake_request(self, method, url):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            req = await session.request(method=method, url=url)
            content = await req.read()
            return req.status, content


def _pook_url(URL):
    return pook.head(URL).reply(200).mock


@pytest.fixture
def URL(httpbin):
    return f"{httpbin.url}/status/404"


@pytest.mark.asyncio
async def test_async_with_request(URL):
    mock = _pook_url(URL)
    async with aiohttp.ClientSession() as session:
        async with session.head(URL) as req:
            assert req.status == 200

    assert len(mock.matches) == 1


@pytest.mark.asyncio
async def test_await_request(URL):
    mock = _pook_url(URL)
    async with aiohttp.ClientSession() as session:
        req = await session.head(URL)
        assert req.status == 200

    assert len(mock.matches) == 1


@pytest.mark.asyncio
async def test_binary_body(URL):
    pook.get(URL).reply(200).body(BINARY_FILE)
    async with aiohttp.ClientSession() as session:
        req = await session.get(URL)
        assert await req.read() == BINARY_FILE


@pytest.mark.asyncio
async def test_json_matcher_data_payload(URL):
    payload = {"foo": "bar"}
    pook.post(URL).json(payload).reply(200).body(BINARY_FILE)
    async with aiohttp.ClientSession() as session:
        req = await session.post(URL, data=json.dumps(payload))
        assert await req.read() == BINARY_FILE


@pytest.mark.asyncio
async def test_json_matcher_json_payload(URL):
    payload = {"foo": "bar"}
    pook.post(URL).json(payload).reply(200).body(BINARY_FILE)
    async with aiohttp.ClientSession() as session:
        req = await session.post(URL, json=payload)
        assert await req.read() == BINARY_FILE
