import aiohttp
import pook
import pytest


pytestmark = pytest.mark.asyncio

URL = "https://httpbin.org/status/404"


def _pook_url():
    return pook.head(URL).reply(200).mock


async def test_async_with_request():
    # Cannot use `@pook.on` with pytest marks
    pook.on()
    mock = _pook_url()
    async with aiohttp.ClientSession() as session:
        async with session.head(URL) as req:
            assert req.status == 200
    pook.off()

    assert len(mock.matches) == 1


async def test_await_request():
    # Cannot use `@pook.on` with pytest marks
    pook.on()
    mock = _pook_url()
    async with aiohttp.ClientSession() as session:
        req = await session.head(URL)
        assert req.status == 200
    pook.off()

    assert len(mock.matches) == 1
