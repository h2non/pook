# -*- coding: utf-8 -*-

import re
from pook.regex import isregex_expr, isregex


def test_isregex_expr():
    cases = (
        ('re/[a-z]/', True),
        ('re/[0-9]/', True),
        ('re/[(.*)]/', True),
        ('re//', True),
        ('RE/[0-9]/', False),
        ('/[0-9]/', False),
        ('[0-9]', False),
        ('//', False),
        ('re/', False),
        ('re/[0-1]/-', False),
        ('e/[0-1]/-', False),
        ('e/[0-1]/', False),
        ('', False),
        ([], False),
        (1, False),
        (None, False),
    )

    for case in cases:
        assert isregex_expr(case[0]) is case[1]


def test_isregex():
    cases = (
        (re.compile('[a-z]'), True),
        ('[a-z]', False),
        ('', False),
        ([], False),
        (1, False),
        (None, False),
    )

    for case in cases:
        assert isregex(case[0]) is case[1]
