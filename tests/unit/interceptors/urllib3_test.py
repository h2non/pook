import pytest
import urllib3
import requests

import pook
from tests.unit.fixtures import BINARY_FILE
from tests.unit.interceptors.base import StandardTests


class TestStandardUrllib3(StandardTests):
    def make_request(self, method, url, content=None, headers=None):
        req_headers = {}
        if headers:
            for header, value in headers:
                if header in req_headers:
                    req_headers[header] += f", {value}"
                else:
                    req_headers[header] = value

        http = urllib3.PoolManager()
        response = http.request(method, url, content, headers=req_headers)
        return response.status, response.read(), response.headers


class TestStandardRequests(StandardTests):
    def make_request(self, method, url, content=None, headers=None):
        req_headers = {}
        if headers:
            for header, value in headers:
                if header in req_headers:
                    req_headers[header] += f", {value}"
                else:
                    req_headers[header] = value

        response = requests.request(method, url, data=content, headers=req_headers)
        return response.status_code, response.content, response.headers


@pook.on
def assert_chunked_response(url_404, input_data, expected):
    (pook.get(url_404).reply(201).body(input_data, chunked=True))

    http = urllib3.PoolManager()
    r = http.request("GET", url_404)

    assert r.status == 201

    chunks = list(r.read_chunked())
    assert chunks == expected


def test_chunked_response_list(url_404):
    assert_chunked_response(url_404, ["a", "b", "c"], [b"a", b"b", b"c"])


def test_chunked_response_str(url_404):
    assert_chunked_response(url_404, "text", [b"text"])


def test_chunked_response_byte(url_404):
    assert_chunked_response(url_404, b"byteman", [b"byteman"])


def test_chunked_response_empty(url_404):
    assert_chunked_response(url_404, "", [])


def test_chunked_response_contains_newline(url_404):
    assert_chunked_response(url_404, "newline\r\n", [b"newline\r\n"])


def test_activate_disable():
    original = urllib3.connectionpool.HTTPConnectionPool.urlopen

    interceptor = pook.interceptors.Urllib3Interceptor(pook.MockEngine)
    interceptor.activate()
    interceptor.disable()

    assert urllib3.connectionpool.HTTPConnectionPool.urlopen == original


@pook.on
def test_binary_body(url_404):
    (pook.get(url_404).reply(200).body(BINARY_FILE))

    http = urllib3.PoolManager()
    r = http.request("GET", url_404)

    assert r.read() == BINARY_FILE


@pook.on
def test_binary_body_chunked(url_404):
    (pook.get(url_404).reply(200).body(BINARY_FILE, chunked=True))

    http = urllib3.PoolManager()
    r = http.request("GET", url_404)

    assert list(r.read_chunked()) == [BINARY_FILE]


@pytest.mark.pook
def test_post_with_headers(url_404):
    mock = pook.post(url_404).header("k", "v").reply(200).mock
    http = urllib3.PoolManager(headers={"k": "v"})
    resp = http.request("POST", url_404)
    assert resp.status == 200
    assert len(mock.matches) == 1
