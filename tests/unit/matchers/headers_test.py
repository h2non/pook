import pytest
import re

import pook


@pytest.mark.parametrize(
    ("expected", "requested"),
    (
        pytest.param(
            {"Content-Type": b"application/pdf"},
            {"Content-Type": b"application/pdf"},
            id="Matching binary headers",
        ),
        pytest.param(
            {
                "Content-Type": b"application/pdf",
                "Authentication": "Bearer 123abc",
            },
            {
                "Content-Type": b"application/pdf",
                "Authentication": "Bearer 123abc",
            },
            id="Matching mixed headers",
        ),
        pytest.param(
            {"Authentication": "Bearer 123abc"},
            {"Authentication": "Bearer 123abc"},
            id="Matching string headers",
        ),
        pytest.param(
            {"Content-Type": b"application/pdf"},
            {
                "Content-Type": b"application/pdf",
                "Authentication": "Bearer 123abc",
            },
            id="Non-matching asymetric mixed headers",
        ),
        pytest.param(
            {"Content-Type": b"application/pdf"},
            {"Content-Type": "application/pdf"},
            id="Non-matching header types (matcher binary, request string)",
        ),
        pytest.param(
            {"Content-Type": "application/pdf"},
            {"Content-Type": b"application/pdf"},
            id="Non-matching header types (matcher string, request binary)",
        ),
        pytest.param(
            {"content-type": "application/pdf"},
            {"Content-Type": "application/pdf"},
            id="Non-matching field name casing",
        ),
        pytest.param(
            {}, {"Content-Type": "application/pdf"}, id="Missing matcher header"
        ),
        pytest.param(
            {"Content-Type": "application/pdf".encode("utf-16")},
            {"Content-Type": "application/pdf".encode("utf-16")},
            id="Arbitrary field value encoding",
        ),
        pytest.param(
            {"Content-Type": "re/json/"},
            {"Content-Type": "application/json"},
            id="Regex-format str expectation",
        ),
        pytest.param(
            {"Content-Type": re.compile("json", re.I)},
            {"Content-Type": "APPLICATION/JSON"},
            id="Regex pattern expectation",
        ),
    ),
)
def test_headers_matcher_matching(expected, requested):
    mock = pook.get("https://example.com")
    if expected:
        mock.headers(expected)

    request = pook.Request()
    request.url = "https://example.com"
    if requested:
        request.headers = requested

    matched, explanation = mock.match(request)
    assert matched, explanation


@pytest.mark.parametrize(
    ("expected", "requested", "explanation"),
    (
        pytest.param(
            {"Content-Type": "application/pdf"},
            {},
            ["HeadersMatcher: Header 'Content-Type' not present"],
            id="Missing request header str expectation",
        ),
        pytest.param(
            {"Content-Type": b"application/pdf"},
            {},
            ["HeadersMatcher: Header 'Content-Type' not present"],
            id="Missing request header bytes expectation",
        ),
        pytest.param(
            {"Content-Type": "application/pdf"},
            {"Content-Type": "application/xml"},
            [
                (
                    "HeadersMatcher: 'application/pdf' != 'application/xml'\n"
                    "- application/pdf\n"
                    "?             ^^^\n"
                    "+ application/xml\n"
                    "?             ^^^\n"
                )
            ],
            id="Non-matching values, matching types",
        ),
        pytest.param(
            {"Content-Type": "application/pdf"},
            {"Content-Type": b"application/xml"},
            [
                (
                    "HeadersMatcher: 'application/pdf' != 'application/xml'\n"
                    "- application/pdf\n"
                    "?             ^^^\n"
                    "+ application/xml\n"
                    "?             ^^^\n"
                )
            ],
            id="Non-matching values, str expectation byte actual",
        ),
        pytest.param(
            {"Content-Type": b"application/pdf"},
            {"Content-Type": "application/xml"},
            [
                (
                    "HeadersMatcher: 'application/pdf' != 'application/xml'\n"
                    "- application/pdf\n"
                    "?             ^^^\n"
                    "+ application/xml\n"
                    "?             ^^^\n"
                )
            ],
            id="Non-matching values, bytes expectation str actual",
        ),
        pytest.param(
            {"Content-Type": "re/json/"},
            {"Content-Type": b"application/xml"},
            [
                (
                    "HeadersMatcher: Regex didn't match: 'json' not found in "
                    "'application/xml'"
                )
            ],
            id="Non-matching values, re-format str expectation",
        ),
    ),
)
def test_headers_not_matching(expected, requested, explanation):
    mock = pook.get("https://example.com")
    if expected:
        mock.headers(expected)

    request = pook.Request()
    request.url = "https://example.com"
    if requested:
        request.headers = requested

    matched, actual_explanation = mock.match(request)
    assert not matched
    assert explanation == actual_explanation


@pytest.mark.parametrize(
    ("required_headers", "requested_headers", "should_match"),
    (
        pytest.param(
            ["content-type", "Authorization"],
            {
                "Content-Type": "",
                "authorization": "Bearer NOT A TOKEN",
            },
            True,
            id="case-insensitive-match-with-empty-value",
        ),
        pytest.param(
            ["content-type", "Authorization"],
            {
                "Content-Type": "application/json",
                "authorization": "Bearer NOT A TOKEN",
            },
            True,
            id="case-insensitive-match-with-non-empty-values",
        ),
        pytest.param(
            ["x-requested-with"],
            {
                "content-type": "application/json",
            },
            False,
            id="x-header-missing-with-other-headers",
        ),
        pytest.param(
            ["x-requested-with"],
            {},
            False,
            id="x-header-no-headers",
        ),
        pytest.param(
            ["content-type"],
            {},
            False,
            id="no-headers",
        ),
        pytest.param(
            ["x-requested-with"],
            {"x-requested-with": "com.example.app"},
            True,
            id="x-header-with-value",
        ),
        pytest.param(
            ["x-requested-with"],
            {"x-requested-with": ""},
            True,
            id="x-header-with-empty-value",
        ),
    ),
)
def test_headers_present(required_headers, requested_headers, should_match):
    mock = pook.get("https://example.com").headers_present(required_headers)

    request = pook.Request()
    request.url = "https://example.com"
    request.headers = requested_headers

    matched, explanation = mock.match(request)
    assert matched == should_match, explanation


def test_headers_present_empty_argument():
    with pytest.raises(ValueError):
        pook.get("https://example.com").headers_present([])
