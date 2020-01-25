# -*- coding: utf-8 -*-

import urllib3
import pook


@pook.on
def test_chunked_response_list():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .body(['a', 'b', 'c'], chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['a', 'b', 'c']


@pook.on
def test_chunked_response_str():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .body('text', chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['text']


@pook.on
def test_chunked_response_byte():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .body(b'byteman', chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['byteman']


@pook.on
def test_chunked_response_empty():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .body('', chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == []


@pook.on
def test_chunked_response_contains_newline():
    (pook.get('httpbin.org/foo')
        .reply(204)
        .body('newline\r\n', chunked=True))

    http = urllib3.PoolManager()
    r = http.request('GET', 'httpbin.org/foo')

    assert r.status == 204
    assert list(r.read_chunked()) == ['newline\r\n']
