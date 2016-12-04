# -*- encoding: ascii -*-
"""
Test suite tasks
~~~~~~~~~~~~~~~~

"""

import os as _os

import invoke as _invoke

from . import clean as _clean


@_invoke.task(_clean.pyclean)
def with_coverage(ctx, options=None):
    """ Run the test suite and measure code coverage. """
    with ctx.root_dir():
        pytest(ctx, options=[
            '--cov=%(package)s' % ctx,
            '--cov-config=test.ini',
            '--cov-report=',
            '--no-cov-on-fail',
        ] + (options or []))


@_invoke.task()
def pytest(ctx, options=None):
    """ Run the test suite using py.test """
    with ctx.root_dir():
        if options is None:
            options = []

        command = ['py.test', '-c', 'test.ini', '-vv', '-s',
                   '--doctest-modules', '--color=yes', '--exitfirst']

        for ignored in ctx.test.ignore:
            command.append('--ignore')
            command.append('"%s"' % (ignored
                                     .replace('\\', '\\\\')
                                     .replace('"', '\\"')))
        ctx.run(' '.join(command + options + ['tests']))


@_invoke.task(default=True)
def tox(ctx, rebuild=False):
    """ Run the test suite using tox """
    command = ['tox', '-c', 'test.ini']
    if rebuild:
        command.append('-r')
    with ctx.root_dir():
        ctx.run(' '.join(command))
