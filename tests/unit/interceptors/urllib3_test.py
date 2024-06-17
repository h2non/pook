import urllib3
import pook
import pytest


from tests.unit.interceptors.base import StandardTests
from tests.unit.fixtures import BINARY_FILE


class TestStandardUrllib3(StandardTests):
    def make_request(self, method, url):
        http = urllib3.PoolManager()
        response = http.request(method, url)
        return response.status, response.read()


@pytest.fixture
def URL(httpbin):
    return f"{httpbin.url}/foo"


@pook.on
def assert_chunked_response(URL, input_data, expected):
    (pook.get(URL).reply(204).body(input_data, chunked=True))

    http = urllib3.PoolManager()
    r = http.request("GET", URL)

    assert r.status == 204

    chunks = list(r.read_chunked())
    assert chunks == expected


def test_chunked_response_list(URL):
    assert_chunked_response(URL, ["a", "b", "c"], [b"a", b"b", b"c"])


def test_chunked_response_str(URL):
    assert_chunked_response(URL, "text", [b"text"])


def test_chunked_response_byte(URL):
    assert_chunked_response(URL, b"byteman", [b"byteman"])


def test_chunked_response_empty(URL):
    assert_chunked_response(URL, "", [])


def test_chunked_response_contains_newline(URL):
    assert_chunked_response(URL, "newline\r\n", [b"newline\r\n"])


def test_activate_disable():
    original = urllib3.connectionpool.HTTPConnectionPool.urlopen

    interceptor = pook.interceptors.Urllib3Interceptor(pook.MockEngine)
    interceptor.activate()
    interceptor.disable()

    assert urllib3.connectionpool.HTTPConnectionPool.urlopen == original


@pook.on
def test_binary_body(URL):
    (pook.get(URL).reply(200).body(BINARY_FILE))

    http = urllib3.PoolManager()
    r = http.request("GET", URL)

    assert r.read() == BINARY_FILE


@pook.on
def test_binary_body_chunked(URL):
    (pook.get(URL).reply(200).body(BINARY_FILE, chunked=True))

    http = urllib3.PoolManager()
    r = http.request("GET", URL)

    assert list(r.read_chunked()) == [BINARY_FILE]


@pytest.mark.pook
def test_post_with_headers(URL):
    mock = pook.post(URL).header("k", "v").reply(200).mock
    http = urllib3.PoolManager(headers={"k": "v"})
    resp = http.request("POST", URL)
    assert resp.status == 200
    assert len(mock.matches) == 1
