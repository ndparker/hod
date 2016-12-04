# -*- encoding: ascii -*-
"""
Cleanup tasks
~~~~~~~~~~~~~

"""

import invoke as _invoke


@_invoke.task()
def pyclean(ctx):
    """ Wipe *.py[co] files """
    with ctx.root_dir():
        ctx.run(r'/usr/bin/find . -name "*.py[co]" -exec rm -- {} \;',
                echo=True)
        ctx.run(r'/usr/bin/find . -name __pycache__ '
                r'-prune -exec rm -r -- {} \;', echo=True)


@_invoke.task(pyclean, default=True)
def clean(ctx):
    """ Wipe *.py[co] files and test leftovers """
    with ctx.root_dir():
        ctx.run('/bin/rm -f perfdump.*', echo=True)
        ctx.run('/bin/rm -rf pytest.xml coverage.xml .coverage* '
                '_coverage', echo=True)
        ctx.run('/bin/rm -rf build dist .tox .cache', echo=True)


@_invoke.task
def soclean(ctx):
    """ Wipe *.so files """
    with ctx.root_dir():
        ctx.run(r'/usr/bin/find . -name "*.so" -exec rm -- {} \;',
                echo=True)
