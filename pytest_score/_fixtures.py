# -*- coding: utf-8 -*-

import json
from contextlib import contextmanager

import pytest
from fsc.export import export

from ._score import ScoreSheet
from ._serialize import encode, decode

# _score_sheet_instance = None


@export
@pytest.fixture(scope='session')
def score_sheet(request):
    # print(vars(request).keys())
    # print(request.session)
    # global _score_sheet_instance

    with _store_score(save_file=_get_save_file(request)
                      ) as score_sheet_instance:
        request.session.score_sheet_instance = score_sheet_instance
        score_sheet_instance.rotate()
        yield score_sheet_instance


@contextmanager
def _store_score(save_file):
    try:
        with open(save_file, 'r') as in_file:
            score_sheet_instance = json.load(in_file, object_hook=decode)
    except (IOError, json.decoder.JSONDecodeError):
        score_sheet_instance = ScoreSheet()
    if not isinstance(score_sheet_instance, ScoreSheet):
        score_sheet_instance = ScoreSheet()

    yield score_sheet_instance

    with open(save_file, 'w') as out_file:
        json.dump(score_sheet_instance, out_file, default=encode)


def _get_save_file(request):
    return request.config.rootdir.join('.pytest-score')


@export
@pytest.fixture
def score(request, score_sheet):
    def inner(value, cutoff=None, tag=''):
        score_sheet.add_score(
            value, test_name=_get_test_name(request), tag=tag
        )
        if cutoff is not None:
            assert value >= cutoff

    return inner


def _get_test_name(request):
    """Returns module_name.function_name for a given test"""
    return request.module.__name__ + '/' + request._parent_request._pyfuncitem.name
