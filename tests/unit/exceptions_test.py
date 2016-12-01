# -*- coding: utf-8 -*-

from pook import exceptions as ex


def test_exceptions():
    assert isinstance(ex.PookNoMatches(), Exception)
    assert isinstance(ex.PookInvalidBody(), Exception)
    assert isinstance(ex.PookExpiredMock(), Exception)
    assert isinstance(ex.PookNetworkFilterError(), Exception)
    assert isinstance(ex.PookInvalidArgument(), Exception)
