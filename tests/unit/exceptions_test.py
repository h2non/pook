from pook import exceptions as e


def test_exceptions():
    assert isinstance(e.PookNoMatches(), Exception) is True
    assert isinstance(e.PookInvalidBody(), Exception) is True
    assert isinstance(e.PookExpiredMock(), Exception) is True
    assert isinstance(e.PookNetworkFilterError(), Exception) is True
    assert isinstance(e.PookInvalidArgument(), Exception) is True
