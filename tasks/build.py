# -*- encoding: ascii -*-
"""
Build Tasks
~~~~~~~~~~~

"""

import invoke as _invoke


@_invoke.task(default=True)
def sdist(ctx):
    """ Build source distribution """
    with ctx.root_dir():
        ctx.run('python setup.py sdist')
