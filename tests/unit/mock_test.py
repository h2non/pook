import pytest
from pook.mock import Mock
from pook.request import Request


@pytest.fixture
def mock():
    return Mock()


def matcher(mock):
    return mock.matchers[0]


def test_mock_url(mock):
    mock.url("http://google.es")
    assert str(matcher(mock)) == "http://google.es"


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
