import pytest
import json
import itertools
from textwrap import dedent
import re

import pook
from pook.mock import Mock
from pook.request import Request
from pook.exceptions import PookNoMatches
from urllib.request import urlopen

from tests.unit.fixtures import BINARY_FILE, BINARY_FILE_PATH


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
            marks=pytest.mark.xfail(
                condition=True,
                reason="Constructor does not have a method for passing `allow_empty` to `param_exists`",
            ),
            id="param_exists_empty_on_request",
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


def test_times(mock):
    url = "https://example.com"
    mock.url(url)
    mock.times(2)

    req = Request(url=url)

    assert mock.match(req) == (True, [])
    assert mock.match(req) == (True, [])
    matches, errors = mock.match(req)
    assert not matches
    assert len(errors) == 1
    assert "Mock matches request but is expired." in errors[0]
    assert repr(mock) in errors[0]


@pytest.mark.pook
def test_times_integrated(httpbin):
    url = f"{httpbin.url}/status/404"
    pook.get(url).times(2).reply(200).body("hello from pook")

    res = urlopen(url)
    assert res.read() == b"hello from pook"

    res = urlopen(url)
    assert res.read() == b"hello from pook"

    with pytest.raises(PookNoMatches, match="Mock matches request but is expired."):
        urlopen(url)


def test_file_matches(httpbin, mock):
    mock.file(BINARY_FILE_PATH)

    req = Request(
        url=httpbin.url,
        body=BINARY_FILE,
    )

    assert mock.match(req) == (True, [])


def test_file_not_matches(httpbin, mock):
    mock.file(BINARY_FILE_PATH)

    req = Request(
        url=httpbin.url,
        body=b"not the binary file you're looking for!",
    )

    matches, errors = mock.match(req)
    assert not matches
    assert len(errors) == 1
    assert errors[0].startswith("BodyMatcher")


@pytest.mark.parametrize(
    "mock_body, request_body",
    # Both sides will always match, regardless of str/bytes
    list(itertools.product((b"hello", "hello"), (b"hello", "hello"))),
)
def test_body_matches(httpbin, mock, mock_body, request_body):
    mock.body(mock_body)
    req = Request(url=httpbin.url, body=request_body)

    assert mock.match(req) == (True, [])


@pytest.mark.parametrize(
    "mock_body, request_body",
    # Neither left nor right side will ever match due to differing contents
    list(itertools.product((b"bytes", "str"), (b"hello bytes", "hello str"))),
)
def test_body_not_matches(httpbin, mock, mock_body, request_body):
    mock.body(mock_body)
    req = Request(url=httpbin.url, body=request_body)

    matches, errors = mock.match(req)
    assert not matches
    assert len(errors) == 1
    assert errors[0].startswith("BodyMatcher: ")


def test_body_matches_string_regex(httpbin, mock):
    mock.body(re.compile(r"hello, me!"))
    req = Request(
        url=httpbin.url,
        body="This is a big sentence... hello, me! wow, another part",
    )

    assert mock.match(req) == (True, [])


def test_body_matches_bytes_regex(httpbin, mock):
    mock.body(re.compile(rb"hello, me!"))
    req = Request(
        url=httpbin.url,
        body="This is a big sentence... hello, me! wow, another part",
    )

    assert mock.match(req) == (True, [])


def test_xml_matches(httpbin, mock):
    xml = dedent(
        """
        <?xml version="1.0"?>

        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
            <dc:title>A pook test for XML!</dc:title>
        </metadata>
        """
    ).strip()
    mock.xml(xml)

    req = Request(
        url=httpbin.url,
        xml=xml,
    )

    assert mock.match(req) == (True, [])


def test_xml_not_matches(httpbin, mock):
    xml = dedent(
        """
        <?xml version="1.0"?>

        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
            <dc:title>A pook test for XML!</dc:title>
        </metadata>
        """
    ).strip()
    mock.xml(xml)

    req = Request(
        url=httpbin.url,
        xml=xml.replace("A pook test for XML!", "Not this one!"),
    )

    matches, errors = mock.match(req)
    assert not matches
    assert len(errors) == 1
    assert errors[0].startswith("XMLMatcher:")
