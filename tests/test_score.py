# -*- coding: utf-8 -*-


# def test_score_fixture(testdir, score):
#     """Make sure that pytest accepts the fixture."""
#
#     # create a temporary pytest test module
#     testdir.makepyfile("""
#         def test_sth(score):
#             pass
#     """)
#
#     # run pytest with the following cmd args
#     result = testdir.runpytest(
#         '-v',
#     )
#
#     # fnmatch_lines does an assertion internally
#     result.stdout.fnmatch_lines([
#         '*::test_sth PASSED*',
#     ])
#
#     # make sure that that we get a '0' exit code for the testsuite
#     assert result.ret == 0

def test_score(score, score_sheet):
    score(1., tag='bla')
