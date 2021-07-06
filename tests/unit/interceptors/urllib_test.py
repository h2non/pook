# -*- coding: utf-8 -*-

import json
from urllib.request import urlopen
import pook
import pytest


@pytest.fixture(autouse=True)
def intercept():
    pook.on()
    yield
    pook.off()


def test_json_response_is_forwarder_successfuly():
    (pook.get("httpjson.org/foo").reply(200).json({}))
    r = urlopen("http://httpjson.org/foo")
    assert r.status == 200
    assert json.load(r) == {}


@pytest.mark.parametrize(
    'data,expected',
    [('data', 'data'), (b'data', 'data')]
)
def test_binary_response_can_be_decoded(data, expected):
    (pook.get("httpbin.org/foo").reply(200).body(data))
    r = urlopen("http://httpbin.org/foo")
    assert r.status == 200
    assert r.read().decode() == expected
