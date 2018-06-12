# -*- coding: utf-8 -*-

from contextlib import contextmanager

import yaml

import pytest

from ._score import ScoreSheet

#
# def pytest_addoption(parser):
#     group = parser.getgroup('score')

@pytest.fixture(scope='session')
def score_sheet(request):
    with _store_score(save_file=_get_save_file(request)) as score_sheet:
        yield score_sheet

@pytest.fixture
def score(request, score_sheet):
    def inner(value, tag=''):
        score_sheet.add_score(value, test_name=_get_test_name(request), tag=tag)
    return inner

def _get_test_name(request):
    """Returns module_name.function_name for a given test"""
    return request.module.__name__ + '/' + request._parent_request._pyfuncitem.name

def _get_save_file(request):
    return request.config.rootdir.join('.pytest-score')

@contextmanager
def _store_score(save_file):
    try:
        with open(save_file, 'r') as in_file:
            score_sheet = yaml.load(in_file)
    except (IOError, yaml.parser.ParserError):
        score_sheet = ScoreSheet()

    yield score_sheet

    with open(save_file, 'w') as out_file:
        yaml.dump(score_sheet, out_file)
