# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('score')
    group.addoption(
        '--strict-score',
        action='store_true',
        dest='dest_strict_score',
        help='Disallow scores without a cut-off threshold.'
    )

@pytest.fixture
def bar(request):
    return request.config.option.dest_strict_score
