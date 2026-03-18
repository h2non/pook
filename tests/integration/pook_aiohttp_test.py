import pytest
import aiohttp

import pook

pytestmark = [pytest.mark.pook]


async def test_aiohttp_match_body():
    body = {"foo": "bar"}
    pook.post("http://example.com", body="foo=1").reply(200).json(body)
    res = await aiohttp.ClientSession().post("http://example.com", data={"foo": 1})
    assert res.status == 200
    assert res.headers == {"Content-Type": "application/json"}
    assert await res.json() == body
