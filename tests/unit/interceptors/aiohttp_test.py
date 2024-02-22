import sys

import pook
import pytest

from pathlib import Path

SUPPORTED = sys.version_info < (3, 12)
if SUPPORTED:
    # See pyproject.toml comment
    import aiohttp


pytestmark = [
    pytest.mark.pook
]


binary_file = (Path(__file__).parents[1] / "fixtures" / "nothing.bin").read_bytes()


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
    pook.get(URL).reply(200).body(binary_file, binary=True)
    async with aiohttp.ClientSession() as session:
        req = await session.get(URL)
        assert await req.read() == binary_file
