"""
Defines the reporters to write the score report to the terminal and HTML output, and adds them to the pytest run.
"""

import os
import shutil

import jinja2
from fsc.export import export  # pylint: disable=import-error

from ._score import ScoreStates


@export
def pytest_addoption(parser):
    parser.addoption(
        '--wipe-scores',
        action='store_true',
        help='Delete previous score results.'
    )


@export
def pytest_configure(config):  # pylint: disable=missing-docstring
    config._score_html = HTMLScoreReporter(config)  # pylint: disable=protected-access
    config._score_terminal = TerminalScoreReporter(config)  # pylint: disable=protected-access
    config.pluginmanager.register(config._score_html)  # pylint: disable=protected-access
    config.pluginmanager.register(config._score_terminal)  # pylint: disable=protected-access


@export
def pytest_unconfigure(config):
    config.pluginmanager.unregister(config._score_html)  # pylint: disable=protected-access
    config.pluginmanager.unregister(config._score_terminal)  # pylint: disable=protected-access


class HTMLScoreReporter:
    """
    Saves the score report to an HTML file.
    """

    def __init__(self, config):
        self.save_dirname = str(config.rootdir.join('htmlscore'))

        env = jinja2.Environment(
            loader=jinja2.PackageLoader('pytest_score', 'templates')
        )
        env.globals.update(zip=zip)
        templates_dirpath = os.path.join(
            os.path.dirname(__file__), 'templates'
        )
        self.template = env.get_template('html_template.html')
        self.css_path = os.path.join(templates_dirpath, 'theme.css')

    def pytest_sessionfinish(self, session):
        """
        Method which is called pytest at the end of the session.
        """
        if hasattr(session, '_score_sheet_instance'):
            self._save_html(session._score_sheet_instance)  # pylint: disable=protected-access

    def _save_html(self, score_sheet):
        """
        Saves the HTML and CSS files for the given score sheet.
        """
        os.makedirs(self.save_dirname, exist_ok=True)
        with open(os.path.join(self.save_dirname, 'index.html'),
                  'w') as html_file:
            html_file.write(self._render_template(score_sheet))
        shutil.copyfile(
            self.css_path, os.path.join(self.save_dirname, 'theme.css')
        )

    def _render_template(self, score_sheet):
        header, table, states = score_sheet.create_table()
        return self.template.render(header=header, table=table, states=states)


class TerminalScoreReporter:
    """
    Writes the score report to the terminal.
    """

    def __init__(self, config, file=None):
        import _pytest.config
        self.config = config
        self._tw = _pytest.config.create_terminal_writer(config, file)

    def _write_report(self, score_sheet):
        """
        Write the score report to the terminal.
        """
        header, table, states = score_sheet.create_table()
        table_str = [[str(val) for val in line] for line in table]

        lengths = ((len(val) for val in line) for line in [header] + table_str)
        lengths_max = [max(vals) for vals in zip(*lengths)]
        widths = [l + 4 for l in lengths_max]
        width_total = sum(widths)

        format_str = ''.join('{:<' + str(w) + '}' for w in widths)

        self._tw.line()
        self._tw.line()
        self._tw.sep(sepchar='=', title='Score Sheet')
        self._tw.line()
        self._tw.line(format_str.format(*header))
        self._tw.line('-' * width_total)

        markup_lookup = {
            ScoreStates.BETTER: {
                'green': True
            },
            ScoreStates.WORSE: {
                'red': True,
                'bold': True
            }
        }
        for line, state in zip(table_str, states):
            self._tw.line(
                format_str.format(*line), **markup_lookup.get(state, {})
            )
        self._tw.line('=' * width_total)

    def pytest_sessionfinish(self, session):
        """
        Method which is called pytest at the end of the session.
        """
        if hasattr(session, '_score_sheet_instance'):
            self._write_report(session._score_sheet_instance)  # pylint: disable=protected-access
