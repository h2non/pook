# -*- coding: utf-8 -*-

import urllib3
import pook


@pook.on
def assert_chunked_response(input_data, expected):
    (pook.get('httpbin.org/foo')
        .reply(204)
        .body(input_data, chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204

    # py2 returns decoded chunks, while py3 does not
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
