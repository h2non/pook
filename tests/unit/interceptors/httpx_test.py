import pook
import httpx
import pytest

from itertools import zip_longest


URL = "https://httpbin.org/status/404"


pytestmark = [pytest.mark.pook]


def test_sync():
    pook.get(URL).times(1).reply(200).body("123")

    response = httpx.get(URL)

    assert response.status_code == 200


async def test_async():
    pook.get(URL).times(1).reply(200).body(b"async_body", binary=True).mock

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)

    assert response.status_code == 200
    assert (await response.aread()) == b"async_body"


def test_json():
    (
        pook.post(URL)
        .times(1)
        .json({"id": "123abc"})
        .reply(200)
        .json({"title": "123abc title"})
    )

    response = httpx.post(URL, json={"id": "123abc"})

    assert response.status_code == 200
    assert response.json() == {"title": "123abc title"}


def test_streaming():
    streamed_response = b"streamed response"
    pook.get(URL).times(1).reply(200).body(streamed_response).mock

    with httpx.stream("GET", URL) as r:
        read_bytes = list(r.iter_bytes(chunk_size=1))

    assert len(read_bytes) == len(streamed_response)
    assert bytes().join(read_bytes) == streamed_response


def test_redirect_following():
    urls = [URL, f"{URL}/redirected", f"{URL}/redirected_again"]
    for req, dest in zip_longest(urls, urls[1:], fillvalue=None):
        if not dest:
            pook.get(req).times(1).reply(200).body("found at last")
        else:
            pook.get(req).times(1).reply(302).header("Location", dest)

    response = httpx.get(URL, follow_redirects=True)

    assert response.status_code == 200
    assert response.read() == b"found at last"
