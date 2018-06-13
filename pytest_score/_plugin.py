from pluggy import PluginManager


def pytest_configure(config):
    config._score_html = HTMLScoreReporter()
    config._score_terminal = TerminalScoreReporter(config)
    config.pluginmanager.register(config._score_html)
    config.pluginmanager.register(config._score_terminal)


def pytest_unconfigure(config):
    config.pluginmanager.unregister(config._score_html)
    config.pluginmanager.unregister(config._score_terminal)


class HTMLScoreReporter:
    def pytest_sessionfinish(self, session):
        print('finishing session')


class TerminalScoreReporter:
    def __init__(self, config, file=None):
        import _pytest.config
        self.config = config
        self._tw = _pytest.config.create_terminal_writer(config, file)

    def _write_report(self, score_sheet):
        header, table = score_sheet.create_table()
        table_str = [[str(val) for val in line] for line in table]

        lengths = ((len(val) for val in line) for line in [header] + table_str)
        lengths_max = [max(vals) for vals in zip(*lengths)]
        widths = [l + 4 for l in lengths_max]
        width_total = sum(widths)

        format_str = ''.join('{:<' + str(w) + '}' for w in widths)

        self._tw.line()
        self._tw.sep(sepchar='=', title='Score Sheet')
        self._tw.line(format_str.format(*header))
        self._tw.line('-' * width_total)
        for line in table_str:
            self._tw.line(format_str.format(*line))
        self._tw.line('=' * width_total)

    def pytest_sessionfinish(self, session):
        self._write_report(session.score_sheet_instance)
        # print(session.score_sheet_instance)
