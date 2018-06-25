"""
Defines the container classes for storing the state of the scores.
"""

import warnings
import operator
from enum import Enum
from types import MappingProxyType
from collections import deque


class ScoreSheet:
    """
    Container for the state of all scores.
    """

    def __init__(self, *, history_length=5, scores=MappingProxyType({})):
        self._scores = dict(scores)
        self._history_lenght = history_length

    def to_dict(self):
        return {'scores': self._scores, 'history_length': self._history_lenght}

    @classmethod
    def from_dict(cls, input_dict):
        return cls(
            scores=input_dict['scores'],
            history_length=input_dict['history_length']
        )

    def rotate(self):
        """
        Prepare the score sheet for a new scoring run.
        """
        for test_name_result in self._scores.values():
            for tag_result in test_name_result.values():
                tag_result.rotate()

    def add_score(self, value, *, test_name, tag, evaluator):
        """
        Add a value for a given test.
        """
        self._scores.setdefault(test_name, {})
        self._scores[test_name].setdefault(
            tag, ScoreResult(evaluator=evaluator)
        )
        score_result = self._scores[test_name][tag]
        if score_result.evaluator != evaluator:
            warnings.warn(
                "Evaluator for score {}:{} changed.".format(test_name, tag)
            )
            score_result.evaluator = evaluator
        score_result.add_score(value)

    def create_table(self):
        """
        Create the table and states of the score sheet.
        """
        header = ('Test name', 'Current', 'Last', 'Best')
        states = []
        res = []
        for test_name, test_name_result in self._scores.items():
            for tag, tag_result in test_name_result.items():
                res.append((
                    test_name + ':' + tag,
                    tag_result.current,
                    tag_result.last,
                    tag_result.best,
                ))
                states.append(tag_result.get_state())
        return header, res, states


class ScoreResult:
    """
    Contains the score result corresponding to a single test / tag pair.
    """

    def __init__(self, *, evaluator, history_length=5):
        self.best = None
        self.current = None
        self.evaluator = evaluator
        self._history = deque([], maxlen=history_length)

    def to_dict(self):
        """
        Deconstruct the object into a dictionary.
        """
        return dict(
            best=self.best,
            current=self.current,
            history=list(self._history),
            history_length=self._history.maxlen,
            evaluator=self.evaluator
        )

    @classmethod
    def from_dict(cls, input_dict):
        """
        Reconstruct the object from a dictionary.
        """
        res = cls(
            history_length=input_dict['history_length'],
            evaluator=input_dict['evaluator']
        )
        res._history.extend(input_dict['history'])  # pylint: disable=protected-access
        res.current = input_dict['current']
        res.best = input_dict['best']
        return res

    @property
    def last(self):
        """
        Return the last score.
        """
        try:
            return self._history[0]
        except IndexError:
            return None

    def add_score(self, value):
        """
        Add the given value to the score.
        """
        assert self.current is None, "Cannot assign a score for the same test and tag twice."
        self.current = value
        self.evaluator.assert_sufficient(value)

    def rotate(self):
        """
        Evaluate the best value and flush the current value.
        """
        self.evaluate_best()
        self.flush_current()

    def flush_current(self):
        """
        Flushes the current value, and adds it to the history.
        """
        self._history.appendleft(self.current)
        self.current = None

    def evaluate_best(self):
        """
        Updates the best value.
        """
        self.best = self.evaluator.evaluate_best([
            self.current, self.best, *self._history
        ])

    def get_state(self):
        """
        Get the state of the score.
        """
        return self.evaluator.get_state(current=self.current, best=self.best)


class Evaluator:
    """
    Contains the logic that evaluates score values, for example checking which
    is the best value, and whether a given value meets the cutoff criterion.
    """

    def __init__(self, *, less_is_better=False, cutoff=None):
        self.less_is_better = less_is_better
        self.cutoff = cutoff
        self.better_than_op = operator.lt if self.less_is_better else operator.gt
        self.better_than_or_eqal_op = operator.le if self.less_is_better else operator.ge

    def to_dict(self):
        """
        Deconstruct the object into a dictionary.
        """
        res = {'less_is_better': self.less_is_better}
        if self.cutoff is not None:
            res['cutoff'] = self.cutoff
        return res

    @classmethod
    def from_dict(cls, input_dict):
        """
        Reconstruct the object from a dictionary.
        """
        return cls(
            less_is_better=input_dict['less_is_better'],
            cutoff=input_dict.get('cutoff', None),
        )

    def evaluate_best(self, values):
        """
        Evaluate the best of a given list of values.
        """
        values_not_none = [val for val in values if val is not None]
        if not values_not_none:
            return None
        if self.less_is_better:
            return min(values_not_none)
        return max(values_not_none)

    def assert_sufficient(self, value):
        """
        Check if the value is sufficient, and raise an AssertionError if it doesn't.
        """
        if self.cutoff is not None:
            assert self.better_than_or_eqal_op(value, self.cutoff)

    def __eq__(self, other):
        return (self.less_is_better == other.less_is_better
                ) and (self.cutoff == other.cutoff)

    def get_state(self, current, best):
        """
        Evaluate the state of the score, given the current and best values.
        """
        try:
            if self.better_than_op(current, best):
                return ScoreStates.BETTER
            elif self.better_than_op(best, current):
                return ScoreStates.WORSE
            return ScoreStates.UNCHANGED
        except TypeError:
            return ScoreStates.UNKNOWN


class ScoreStates(Enum):
    """
    Possible states of the current score versus the best best score.
    """
    UNKNOWN = 'unknown'
    UNCHANGED = 'unchanged'
    BETTER = 'better'
    WORSE = 'worse'
