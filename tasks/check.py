# -*- encoding: ascii -*-
"""
Checking tasks
~~~~~~~~~~~~~~

"""

from . import clean as _clean

import invoke as _invoke


@_invoke.task(_clean.pyclean, default=True)
def lint(ctx):
    """ Run pylint """
    with ctx.root_dir():
        ctx.run('pylint --rcfile pylintrc "%(package)s"' % ctx, echo=True)
