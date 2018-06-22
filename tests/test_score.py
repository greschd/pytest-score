# -*- coding: utf-8 -*-
"""
Basic test using the ``pytest-score`` plugin.
"""


def test_score(score):
    score(3.1, tag='test')
    score(2., tag='test2', less_is_better=True)
