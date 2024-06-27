import pook
import httpx
import pytest

from itertools import zip_longest

from tests.unit.interceptors.base import StandardTests


pytestmark = [pytest.mark.pook]


class TestStandardAsyncHttpx(StandardTests):
    is_async = True

    async def amake_request(self, method, url):
        async with httpx.AsyncClient() as client:
            response = await client.request(method=method, url=url)
            content = await response.aread()
            return response.status_code, content


class TestStandardSyncHttpx(StandardTests):
    def make_request(self, method, url):
        response = httpx.request(method=method, url=url)
        content = response.read()
        return response.status_code, content


@pytest.fixture
def URL(httpbin):
    return f"{httpbin.url}/status/404"


def test_sync(URL):
    pook.get(URL).times(1).reply(200).body("123")

    response = httpx.get(URL)

    assert response.status_code == 200


async def test_async(URL):
    pook.get(URL).times(1).reply(200).body(b"async_body").mock

    async with httpx.AsyncClient() as client:
        response = await client.get(URL)

    assert response.status_code == 200
    assert (await response.aread()) == b"async_body"


def test_json(URL):
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


@pytest.mark.parametrize("response_method", ("iter_bytes", "iter_raw"))
def test_streaming(URL, response_method):
    streamed_response = b"streamed response"
    pook.get(URL).times(1).reply(200).body(streamed_response).mock

    with httpx.stream("GET", URL) as r:
        read_bytes = list(getattr(r, response_method)(chunk_size=1))

    assert len(read_bytes) == len(streamed_response)
    assert bytes().join(read_bytes) == streamed_response


def test_redirect_following(URL):
    urls = [URL, f"{URL}/redirected", f"{URL}/redirected_again"]
    for req, dest in zip_longest(urls, urls[1:], fillvalue=None):
        if not dest:
            pook.get(req).times(1).reply(200).body("found at last")
        else:
            pook.get(req).times(1).reply(302).header("Location", dest)

    response = httpx.get(URL, follow_redirects=True)

    assert response.status_code == 200
    assert response.read() == b"found at last"
