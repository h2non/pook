import warnings
from urllib.request import urlopen

import pytest

import pook


pytestmark = [
    pytest.mark.undo_suppress_own_warnings,
    pytest.mark.pook,
]


def test_deprecation_warning_fixed_no_binary_arg(httpbin):
    with warnings.catch_warnings(record=True) as recorded_warnings:
        # Best case scenario
        url = f"{httpbin.url}/status/404"
        pook.get(url).param("was", "not_bytes").reply(200).body("hello from pook")
        pook.get(url).param("was", "bytes").reply(200).body(
            b"hello with bytes argument"
        )

        res = urlopen(f"{url}?was=bytes")
        assert res.read() == b"hello with bytes argument"

        res = urlopen(f"{url}?was=not_bytes")
        assert res.read() == b"hello from pook"

    assert recorded_warnings == []


def test_deprecation_warning_fixed_binary_True(httpbin):
    with warnings.catch_warnings(record=True) as recorded_warnings:
        # Best case scenario
        url = f"{httpbin.url}/status/404"
        pook.get(url).reply(200).body(b"hello from pook", binary=True)

        res = urlopen(url)
        assert res.read() == b"hello from pook"

    assert len(recorded_warnings) == 1
    assert "The fix is already applied, but `binary` was passed to `.body()`." in str(
        recorded_warnings[0].message
    )


def test_deprecation_warning_fixed_binary_False(httpbin):
    with warnings.catch_warnings(record=True) as recorded_warnings:
        # Best case scenario
        url = f"{httpbin.url}/status/404"
        pook.get(url).reply(200).body("hello from pook", binary=False)

        res = urlopen(url)
        assert res.read() == "hello from pook"

    assert len(recorded_warnings) == 1
    assert "The fix is already applied, but `binary` was passed to `.body()`." in str(
        recorded_warnings[0].message
    )


def test_deprecation_warning_unapplied_fix_no_arg(httpbin, without_binary_body_fix):
    with warnings.catch_warnings(record=True) as recorded_warnings:
        # Best case scenario
        url = f"{httpbin.url}/status/404"
        pook.get(url).reply(200).body("hello from pook")

        res = urlopen(url)
        assert res.read() == "hello from pook"

    assert len(recorded_warnings) == 1
    message = str(recorded_warnings[0].message)
    assert "Support for them will be removed in the next major version" in message
    assert "from this call to `.body()`" not in message


def test_deprecation_warning_unapplied_fix_binary_True(
    httpbin, without_binary_body_fix
):
    with warnings.catch_warnings(record=True) as recorded_warnings:
        # Best case scenario
        url = f"{httpbin.url}/status/404"
        pook.get(url).reply(200).body(b"hello from pook", binary=True)

        res = urlopen(url)
        assert res.read() == b"hello from pook"

    assert len(recorded_warnings) == 1
    message = str(recorded_warnings[0].message)
    assert "Support for them will be removed in the next major version" in message
    assert "and remove `binary=True` from this call to `.body()`" in message


def test_deprecation_warning_unapplied_fix_binary_False(
    httpbin, without_binary_body_fix
):
    with warnings.catch_warnings(record=True) as recorded_warnings:
        # Best case scenario
        url = f"{httpbin.url}/status/404"
        pook.get(url).reply(200).body("hello from pook", binary=False)

        res = urlopen(url)
        assert res.read() == "hello from pook"

    assert len(recorded_warnings) == 1
    message = str(recorded_warnings[0].message)
    assert "Support for them will be removed in the next major version" in message
    assert "and remove `binary=False` from this call to `.body()`" in message
