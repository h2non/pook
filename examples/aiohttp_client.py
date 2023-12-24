# flake8: noqa

import pook
import aiohttp
import asyncio
import async_timeout


async def fetch(session, url, data):
    with async_timeout.timeout(10):
        async with session.get(url, data=data) as res:
            print("Status:", res.status)
            print("Headers:", res.headers)
            print("Body:", await res.text())


with pook.use(network=True):
    pook.get(
        "http://httpbin.org/ip",
        reply=404,
        response_type="json",
        response_headers={"Server": "nginx"},
        response_json={"error": "not found"},
    )

    async def main(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            await fetch(session, "http://httpbin.org/ip", bytearray("foo bar", "utf-8"))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
