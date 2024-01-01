import pytest
import json

import pook
from pook.mock import Mock
from pook.request import Request
from urllib.request import urlopen


@pytest.fixture
def mock():
    return Mock()


def matcher(mock):
    return mock.matchers[0]


def test_mock_url(mock):
    mock.url("http://google.es")
    assert str(matcher(mock)) == "http://google.es"


@pytest.mark.parametrize(
    ("param_kwargs", "query_string"),
    (
        pytest.param({"params": {"x": "1"}}, "?x=1", id="params"),
        pytest.param(
            {"param": ("y", "pook")},
            "?y=pook",
            marks=pytest.mark.xfail(
                condition=True,
                reason="Constructor does not correctly handle multi-argument methods from kwargs",
            ),
            id="param",
        ),
        pytest.param(
            {"param_exists": "z"},
            "?z",
            id="param_exists_empty_on_request",
        ),
        pytest.param(
            {"param_exists": "z"},
            "?z=",
            id="param_exists_empty_on_request_with_=",
        ),
        pytest.param(
            {"param_exists": "z"},
            "?z=123",
            id="param_exists_has_value",
        ),
    ),
)
def test_mock_constructor(param_kwargs, query_string):
    # Should not raise
    mock = Mock(
        url="https://httpbin.org/404",
        reply_status=200,
        response_json={"hello": "from pook"},
        **param_kwargs,
    )

    with pook.use():
        pook.engine().add_mock(mock)
        res = urlopen(f"https://httpbin.org/404{query_string}")
        assert res.status == 200
        assert json.loads(res.read()) == {"hello": "from pook"}


@pytest.mark.parametrize(
    "url, params, req, expected",
    [
        ("http://google.es", {}, Request(url="http://google.es"), (True, [])),
        (
            "http://google.es",
            {},
            Request(url="http://google.es?foo=bar"),
            (True, []),
        ),
        (
            "http://google.es",
            {},
            Request(url="http://google.es?foo=bar&baz=qux"),
            (True, []),
        ),
        (
            "http://google.es",
            {},
            Request(url="http://google.es?baz=qux"),
            (True, []),
        ),
        (
            "http://google.es",
            {"foo": "bar"},
            Request(url="http://google.es"),
            (False, []),
        ),
        (
            "http://google.es",
            {"foo": "bar"},
            Request(url="http://google.es?foo=bar"),
            (True, []),
        ),
        (
            "http://google.es",
            {"foo": "bar"},
            Request(url="http://google.es?foo=bar&baz=qux"),
            (True, []),
        ),
        (
            "http://google.es",
            {"foo": "bar"},
            Request(url="http://google.es?baz=qux"),
            (False, []),
        ),
    ],
)
def test_mock_params(url, params, req, expected, mock):
    mock.url(url)
    if params:
        mock.params(params)
    assert mock.matchers.match(req) == expected


def test_new_response(mock):
    assert mock.reply() != mock.reply(new_response=True, json={})
