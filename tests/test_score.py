# -*- coding: utf-8 -*-

# © 2015-2018, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Basic test using the ``pytest-score`` plugin.
"""


def test_score(score):
    score(3.1, tag='test')
    score(2., tag='test2', less_is_better=True)
