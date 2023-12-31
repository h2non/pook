import pook
import pytest
import requests


@pytest.mark.pook
def test_requests_get():
    body = {"error": "not found"}
    pook.get("http://foo.com").reply(404).json(body)

    res = requests.get("http://foo.com")
    assert res.status_code == 404
    assert res.headers == {"Content-Type": "application/json"}
    assert res.json() == body


@pytest.mark.pook
def test_requests_match_url():
    body = {"foo": "bar"}
    pook.get("http://foo.com").reply(200).json(body)

    res = requests.get("http://foo.com")
    assert res.status_code == 200
    assert res.headers == {"Content-Type": "application/json"}
    assert res.json() == body


@pytest.mark.pook
def test_requests_match_query_params():
    body = {"foo": "bar"}
    (pook.get("http://foo.com").params({"foo": "bar"}).reply(200).json(body))

    res = requests.get("http://foo.com", params={"foo": "bar"})
    assert res.status_code == 200
    assert res.headers == {"Content-Type": "application/json"}
    assert res.json() == body


def test_pook_use_context_manager_is_disabled_after_exit():
    url = "http://pook.local.not-a-thing"
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get(url)
    respJson = {"resp": "ok"}
    with pook.use():
        pook.get(url).reply().json(respJson)
        resp = requests.get(url)
        assert resp.json() == respJson
        assert pook.isdone()
    assert not pook.isactive()
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get(url)
