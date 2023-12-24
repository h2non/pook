import pook
import requests


@pook.activate
def test_simple_pook_request():
    pook.get("server.com/foo").reply(204)
    res = requests.get("http://server.com/foo")
    assert res.status_code == 204


@pook.on
def test_enable_engine():
    pook.get("server.com/foo").reply(204)
    res = requests.get("http://server.com/foo")
    assert res.status_code == 204


@pook.get("server.com/foo", reply=204)
def test_decorator():
    res = requests.get("http://server.com/foo")
    assert res.status_code == 204


def test_context_manager():
    with pook.use():
        pook.get("server.com/bar", reply=204)
        res = requests.get("http://server.com/bar")
        assert res.status_code == 204


@pook.on
def test_no_match_exception():
    pook.get("server.com/bar", reply=204)
    try:
        requests.get("http://server.com/baz")
    except Exception:
        pass
    else:
        raise RuntimeError("expected to fail")
