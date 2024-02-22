import urllib3
import pook
import pytest

from pathlib import Path


binary_file = (Path(__file__).parents[1] / "fixtures" / "nothing.bin").read_bytes()


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
    chunks = [c.decode() if isinstance(c, bytes) else c for c in chunks]
    assert chunks == expected


def test_chunked_response_list(URL):
    assert_chunked_response(URL, ["a", "b", "c"], ["a", "b", "c"])


def test_chunked_response_str(URL):
    assert_chunked_response(URL, "text", ["text"])


def test_chunked_response_byte(URL):
    assert_chunked_response(URL, b"byteman", ["byteman"])


def test_chunked_response_empty(URL):
    assert_chunked_response(URL, "", [])


def test_chunked_response_contains_newline(URL):
    assert_chunked_response(URL, "newline\r\n", ["newline\r\n"])


def test_activate_disable():
    original = urllib3.connectionpool.HTTPConnectionPool.urlopen

    interceptor = pook.interceptors.Urllib3Interceptor(pook.MockEngine)
    interceptor.activate()
    interceptor.disable()

    assert urllib3.connectionpool.HTTPConnectionPool.urlopen == original


@pook.on
def test_binary_body(URL):
    (pook.get(URL).reply(200).body(binary_file, binary=True))

    http = urllib3.PoolManager()
    r = http.request("GET", URL)

    assert r.read() == binary_file


@pook.on
def test_binary_body_chunked(URL):
    (pook.get(URL).reply(200).body(binary_file, binary=True, chunked=True))

    http = urllib3.PoolManager()
    r = http.request("GET", URL)

    assert list(r.read_chunked()) == [binary_file]


@pytest.mark.pook
def test_post_with_headers(URL):
    mock = pook.post(URL).header("k", "v").reply(200).mock
    http = urllib3.PoolManager(headers={"k": "v"})
    resp = http.request("POST", URL)
    assert resp.status == 200
    assert len(mock.matches) == 1
