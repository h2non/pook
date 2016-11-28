# -*- coding: utf-8 -*-

import pook
import pytest
import requests


@pytest.fixture
def mock():
    pook.activate()
    yield pook
    pook.disable()


def test_requests_get(mock):
    body = {'error': 'not found'}
    mock.get('http://foo.com').reply(404).json(body)

    res = requests.get('http://foo.com')
    assert res.status_code == 404
    assert res.headers == {'Content-Type': 'application/json'}
    assert res.json() == body
    assert pook.isdone() is True


def test_requests_match_url(mock):
    body = {'foo': 'bar'}
    mock.get('http://foo.com').reply(200).json(body)

    res = requests.get('http://foo.com')
    assert res.status_code == 200
    assert res.headers == {'Content-Type': 'application/json'}
    assert res.json() == body
    assert pook.isdone() is True
