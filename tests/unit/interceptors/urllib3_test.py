# -*- coding: utf-8 -*-

import urllib3
import pook


@pook.on
def test_chunked_response_list():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .header('Transfer-Encoding', 'chunked')
        .body(['a', 'b', 'c']))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['a', 'b', 'c']


@pook.on
def test_chunked_response_str():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .header('Transfer-Encoding', 'chunked')
        .body('text'))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['text']


@pook.on
def test_chunked_response_byte():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .header('Transfer-Encoding', 'chunked')
        .body(b'byteman'))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['byteman']


@pook.on
def test_chunked_response_empty():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .header('Transfer-Encoding', 'chunked')
        .body(''))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == []
