from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

import pook
from tests.unit.interceptors.base import StandardTests


class TestUrllib(StandardTests):
    def make_request(self, method, url, content=None):
        request = Request(
            url=url,
            method=method,
            data=content,
        )
        try:
            response = urlopen(request)
            return response.status, response.read()
        except HTTPError as e:
            return e.code, e.msg


@pytest.mark.pook
def test_urllib_ssl():
    pook.get("https://example.com").reply(200).body("Hello from pook")
    res = urlopen("https://example.com")

    assert res.read() == b"Hello from pook"


@pytest.mark.pook
def test_urllib_clear():
    pook.get("http://example.com").reply(200).body("Hello from pook")
    res = urlopen("http://example.com")

    assert res.read() == b"Hello from pook"
