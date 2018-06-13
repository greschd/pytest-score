# -*- coding: utf-8 -*-
"""
Basic test using the ``pytest-score`` plugin.
"""


def test_score(score):
    score(2., tag='test')
    score(1., tag='test2')
