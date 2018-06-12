from collections import defaultdict, deque

import yaml

class ScoreSheet:
    def __init__(self, *, history_length=5):
        self._tests = defaultdict(
            _create_test_name_result
        )

    def rotate(self):
        for test_name_result in self._tests.values():
            for tag_result in test_name_results.values():
                tag_result.rotate()

    def add_score(self, value, *, test_name, tag):
        self._tests[test_name][tag].add_score(value)

def _create_test_name_result():
    return defaultdict(ScoreResult)

# def _create_tag_result():


class ScoreResult:
    def __init__(self, *, history_length=5):
        self.best = None
        self.current = None
        self._history = deque([], maxlen=history_length)

    @property
    def last(self):
        return self._history[0]

    def add_score(self, value):
        assert self.current is None, "Cannot assign a score for the same test and tag twice."
        self.current = value

    def rotate(self):
        self.evaluate_best()
        self.flush_current()

    def flush_current(self):
        self.current = None

    def evaluate_best(self):
        values = [self.current, self.best, *self._history]
        values_not_none = [val for val in values if val is not None]
        if values_not_none:
            self.best = max(values_not_none)
