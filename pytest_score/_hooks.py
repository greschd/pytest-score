# -*- coding: utf-8 -*-

import pytest
from py.xml import html

# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
# from ._fixtures import _score_sheet_instance
# header, table_content = _score_sheet_instance.create_table()
#
# header_classes = [
#     ('sortable', 'asc', 'initial-sort', 'active'),
#     ('sortable', 'asc', 'numeric', 'inactive'),
#     ('sortable', 'asc', 'numeric', 'inactive'),
#     ('sortable', 'asc', 'numeric', 'inactive'),
# ]
# header_classes_str = [' '.join(cl) for cl in header_classes]
# table = html.table(width='100%', border='1px solid #999', color='#fff', **{'class': 'results-table'})
#
# header_items = [html.th(header_item) for header_item, cl in zip(header, header_classes_str)]
# # header_items = [html.th(header_item, **{'class': cl}) for header_item, cl in zip(header, header_classes_str)]
# # for header_item, cl in zip(header_items, header_classes):
#     # setattr(header_item, 'class', cl)
# table.append(html.thead(html.tr(header_items)))
# table.extend([
#     html.tr([
#         html.td(value) for value in line
#     ])
#     for line in table_content
# ])
# summary.extend(html.p(table))
