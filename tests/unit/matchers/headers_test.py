import pytest

import pook


@pytest.mark.parametrize(
    ('expected', 'requested', 'should_match'),
    (
        pytest.param(
            {'Content-Type': b'application/pdf'},
            {'Content-Type': b'application/pdf'},
            True,
            id='Matching binary headers'
        ),
        pytest.param(
            {
                'Content-Type': b'application/pdf',
                'Authentication': 'Bearer 123abc',
            },
            {
                'Content-Type': b'application/pdf',
                'Authentication': 'Bearer 123abc',
            },
            True,
            id='Matching mixed headers'
        ),
        pytest.param(
            {'Authentication': 'Bearer 123abc'},
            {'Authentication': 'Bearer 123abc'},
            True,
            id='Matching string headers'
        ),
        pytest.param(
            {'Content-Type': b'application/pdf'},
            {
                'Content-Type': b'application/pdf',
                'Authentication': 'Bearer 123abc',
            },
            True,
            id='Non-matching asymetric mixed headers'
        ),
        pytest.param(
            {'Content-Type': b'application/pdf'},
            {'Content-Type': 'application/pdf'},
            True,
            id='Non-matching header types (matcher binary, request string)'
        ),
        pytest.param(
            {'Content-Type': 'application/pdf'},
            {'Content-Type': b'application/pdf'},
            True,
            id='Non-matching header types (matcher string, request binary)'
        ),
        pytest.param(
            {'Content-Type': 'application/pdf'},
            {'Content-Type': 'application/xml'},
            False,
            id='Non-matching values'
        ),
        pytest.param(
            {'content-type': 'application/pdf'},
            {'Content-Type': 'application/pdf'},
            True,
            id='Non-matching field name casing'
        ),
        pytest.param(
            {},
            {'Content-Type': 'application/pdf'},
            True,
            id='Missing matcher header'
        ),
        pytest.param(
            {'Content-Type': 'application/pdf'},
            {},
            False,
            id='Missing request header'
        ),
        pytest.param(
            {'Content-Type': 'application/pdf'.encode('utf-16')},
            {'Content-Type': 'application/pdf'.encode('utf-16')},
            True,
            id='Arbitrary field value encoding'
        ),
    )
)
def test_headers_matcher(expected, requested, should_match):
    mock = pook.get('https://example.com')
    if expected:
        mock.headers(expected)

    request = pook.Request()
    request.url = 'https://example.com'
    if requested:
        request.headers = requested

    matched, explanation = mock.match(request)
    assert matched == should_match, explanation


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
            id="case-insensitive-match-with-empty-value"
        ),
        pytest.param(
            ["content-type", "Authorization"],
            {
                "Content-Type": "application/json",
                "authorization": "Bearer NOT A TOKEN",
            },
            True,
            id="case-insensitive-match-with-non-empty-values"
        ),
        pytest.param(
            ["x-requested-with"],
            {
                "content-type": "application/json",
            },
            False,
            id="x-header-missing-with-other-headers"
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
            id="x-header-with-value"
        ),
        pytest.param(
            ["x-requested-with"],
            {"x-requested-with": ""},
            True,
            id="x-header-with-empty-value"
        ),
    )
)
def test_headers_present(required_headers, requested_headers, should_match):
    mock = pook.get('https://example.com').headers_present(required_headers)

    request = pook.Request()
    request.url = 'https://example.com'
    request.headers = requested_headers

    matched, explanation = mock.match(request)
    assert matched == should_match, explanation


def test_headers_present_empty_headers():
    with pytest.raises(ValueError):
        pook.get('https://example.com').headers_present([])
