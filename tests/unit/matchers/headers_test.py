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
