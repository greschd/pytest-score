from collections import defaultdict, deque


class ScoreSheet:
    def __init__(self, *, history_length=5):
        self._scores = defaultdict(
            lambda: defaultdict(lambda: ScoreResult(history_length=history_length))
        )

    def to_dict(self):
        res = {
            key: {k: v
                  for k, v in val.items()}
            for key, val in self._scores.items()
        }
        return res

    @classmethod
    def from_dict(cls, input_dict, *, history_length=5):
        res = cls(history_length=history_length)
        for test_name, test_name_result in input_dict.items():
            for tag, tag_results in test_name_result.items():
                res._scores[test_name][tag] = tag_results
        return res

    def rotate(self):
        for test_name_result in self._scores.values():
            for tag_result in test_name_result.values():
                tag_result.rotate()

    def add_score(self, value, *, test_name, tag):
        self._scores[test_name][tag].add_score(value)

    def create_table(self):
        header = ('Test name', 'Current', 'Last', 'Best')
        res = []
        for test_name, test_name_result in self._scores.items():
            for tag, tag_result in test_name_result.items():
                res.append((
                    test_name + ':' + tag,
                    tag_result.current,
                    tag_result.last,
                    tag_result.best,
                ))
        return header, res


class ScoreResult:
    def __init__(self, *, history_length=5):
        self.best = None
        self.current = None
        self._history = deque([], maxlen=history_length)

    def to_dict(self):
        return dict(
            best=self.best,
            current=self.current,
            history=list(self._history),
            history_length=self._history.maxlen
        )

    @classmethod
    def from_dict(cls, input_dict):
        res = cls(history_length=input_dict['history_length'])
        res._history.extend(input_dict['history'])
        res.current = input_dict['current']
        res.best = input_dict['best']
        return res

    @property
    def last(self):
        try:
            return self._history[0]
        except IndexError:
            return None

    def add_score(self, value):
        assert self.current is None, "Cannot assign a score for the same test and tag twice."
        self.current = value

    def rotate(self):
        self.evaluate_best()
        self.flush_current()

    def flush_current(self):
        self._history.appendleft(self.current)
        self.current = None

    def evaluate_best(self):
        values = [self.current, self.best, *self._history]
        values_not_none = [val for val in values if val is not None]
        if values_not_none:
            self.best = max(values_not_none)
