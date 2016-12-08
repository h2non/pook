# -*- coding: utf-8 -*-

import pook
import pytest
import requests


@pook.activate
def test_simple_pook_request():
    pook.get('server.com/foo').reply(204)
    res = requests.get('http://server.com/foo')
    assert res.status_code == 204


def test_enable_engine():
    pook.get('server.com/foo').reply(204)
    res = requests.get('http://server.com/foo')
    assert res.status_code == 204
    pook.disable()


@pook.get('server.com/bar', reply=204)
def test_decorator():
    res = requests.get('http://server.com/bar')
    assert res.status_code == 204


def test_context_manager():
    with pook.use():
        pook.get('server.com/baz', reply=204)
        res = requests.get('http://server.com/baz')
        assert res.status_code == 204


def test_no_match_exception():
    pook.get('server.com/bar', reply=204)
    with pytest.raises(Exception):
        requests.get('http://server.com/baz')
