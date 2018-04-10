# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('quality')
    group.addoption(
        '--strict-quality',
        action='store_true',
        dest='dest_strict_quality',
        help='Disallow quality criteria without a cut-off threshold.'
    )

@pytest.fixture
def bar(request):
    return request.config.option.dest_strict_quality
