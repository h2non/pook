import pytest
import requests

import pook

pytestmark = [pytest.mark.pook]


def test_requests_get():
    body = {"error": "not found"}
    pook.get("http://foo.com").reply(404).json(body)

    res = requests.get("http://foo.com")
    assert res.status_code == 404
    assert res.headers == {"Content-Type": "application/json"}
    assert res.json() == body


def test_requests_match_url():
    body = {"foo": "bar"}
    pook.get("http://foo.com").reply(200).json(body)

    res = requests.get("http://foo.com")
    assert res.status_code == 200
    assert res.headers == {"Content-Type": "application/json"}
    assert res.json() == body


def test_requests_match_query_params():
    body = {"foo": "bar"}
    (pook.get("http://foo.com").params({"foo": "bar"}).reply(200).json(body))

    res = requests.get("http://foo.com", params={"foo": "bar"})
    assert res.status_code == 200
    assert res.headers == {"Content-Type": "application/json"}
    assert res.json() == body
