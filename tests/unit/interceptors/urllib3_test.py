# -*- coding: utf-8 -*-

import urllib3
import pook

from pathlib import Path


binary_file = (
    Path(__file__).parents[1] / "fixtures" / "nothing.bin"
).read_bytes()


URL = 'https://httpbin.org/foo'


@pook.on
def assert_chunked_response(input_data, expected):
    (pook.get(URL)
        .reply(204)
        .body(input_data, chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', URL)

    assert r.status == 204

    chunks = list(r.read_chunked())
    chunks = [c.decode() if isinstance(c, bytes) else c for c in chunks]
    assert chunks == expected


def test_chunked_response_list():
    assert_chunked_response(['a', 'b', 'c'], ['a', 'b', 'c'])


def test_chunked_response_str():
    assert_chunked_response('text', ['text'])


def test_chunked_response_byte():
    assert_chunked_response(b'byteman', ['byteman'])


def test_chunked_response_empty():
    assert_chunked_response('', [])


def test_chunked_response_contains_newline():
    assert_chunked_response('newline\r\n', ['newline\r\n'])


def test_activate_disable():
    original = urllib3.connectionpool.HTTPConnectionPool.urlopen

    interceptor = pook.interceptors.Urllib3Interceptor(pook.MockEngine)
    interceptor.activate()
    interceptor.disable()

    assert urllib3.connectionpool.HTTPConnectionPool.urlopen == original


@pook.on
def test_binary_body():
    (pook.get(URL)
        .reply(200)
        .body(binary_file, binary=True))

    http = urllib3.PoolManager()
    r = http.request('GET', URL)

    assert r.read() == binary_file


@pook.on
def test_binary_body_chunked():
    (pook.get(URL)
        .reply(200)
        .body(binary_file, binary=True, chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', URL)

    assert list(r.read_chunked()) == [binary_file]
