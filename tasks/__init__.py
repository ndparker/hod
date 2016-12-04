# -*- encoding: ascii -*-
"""
invoke tasks
~~~~~~~~~~~~

"""


def namespace():
    class adict(dict):
        def __init__(self, *args, **kwargs):
            dict.__init__(self, *args, **kwargs)
            self.__dict__ = self

    import contextlib as _contextlib
    import os as _os
    import sys as _sys

    root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

    @_contextlib.contextmanager
    def root_dir():
        old = _os.getcwd()
        try:
            _os.chdir(root)
            yield root
        finally:
            _os.chdir(old)

    env = adict(
        package='hod',
        test=adict(ignore=[]),

        root_dir=root_dir,
    )

    _sys.path.insert(0, _os.path.dirname(
        _os.path.dirname(_os.path.abspath(__file__))
    ))

    class Vars(object):
        from . import (
            build,
            check,
            clean,
            test,
        )

    import invoke as _invoke
    result = _invoke.Collection(*[value for key, value in vars(Vars).items()
                                  if not key.startswith('__')])
    result.configure(env)
    return result

namespace = namespace()
