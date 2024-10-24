from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.client import HTTPResponse

import pytest

import pook
from tests.unit.interceptors.base import StandardTests


class TestUrllib(StandardTests):
    def make_request(self, method, url, content=None, headers=None):
        req_headers = {}
        if headers:
            for header, value in headers:
                if header in req_headers:
                    req_headers[header] += f", {value}"
                else:
                    req_headers[header] = value

        request = Request(
            url=url,
            method=method,
            data=content,
            headers=req_headers,
        )
        try:
            response: HTTPResponse = urlopen(request)
            return response.status, response.read(), response.headers
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
