# -*- coding: utf-8 -*-

from contextlib import contextmanager

import json

import pytest

from ._score import ScoreSheet
from ._serialize import encode, decode


@pytest.fixture(scope='session')
def score_sheet(request):
    with _store_score(save_file=_get_save_file(request)) as score_sheet:
        score_sheet.rotate()
        yield score_sheet


@pytest.fixture
def score(request, score_sheet):
    def inner(value, tag=''):
        score_sheet.add_score(
            value, test_name=_get_test_name(request), tag=tag
        )

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
            score_sheet = json.load(in_file, object_hook=decode)
    except (IOError, json.decoder.JSONDecodeError):
        score_sheet = ScoreSheet()
    if not isinstance(score_sheet, ScoreSheet):
        score_sheet = ScoreSheet()

    yield score_sheet

    with open(save_file, 'w') as out_file:
        json.dump(score_sheet, out_file, default=encode)
