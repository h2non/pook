import pytest
import requests

import pook


@pook.on
def test_simple_pook_request(url_404):
    pook.get(url_404).reply(204)
    res = requests.get(url_404)
    assert res.status_code == 204


@pook.on
def test_enable_engine(url_404):
    pook.get(url_404).reply(204)
    res = requests.get(url_404)
    assert res.status_code == 204
    pook.disable()


def test_decorator(url_404):
    @pook.get(url_404, reply=204)
    def do():
        res = requests.get(url_404)
        assert res.status_code == 204
        return True

    assert do()


def test_context_manager(url_404):
    with pook.use():
        pook.get(url_404, reply=204)
        res = requests.get(url_404)
        assert res.status_code == 204


@pook.on
def test_no_match_exception(url_404, url_401):
    pook.get(url_404, reply=204)
    with pytest.raises(Exception):
        requests.get(url_401)
