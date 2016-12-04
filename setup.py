#!/usr/bin/env python
"""
HOD - Heap On Disk
~~~~~~~~~~~~~~~~~~

"""

import os as _os

from distutils import core as _core
from distutils.command import build_ext as _build_ext
import setuptools as _setuptools

# pylint: disable = invalid-name


def _doc(filename):
    """ Read docs file """
    try:
        with open(_os.path.join('docs', filename)) as fp:
            return fp.read()
    except IOError:
        return None


def _lines(multiline):
    """ Split multiline string into single line % empty and comments """
    return [line for line in (
        line.strip() for line in multiline.splitlines(False)
    ) if line and not line.startswith('#')]


package = dict(
    name='hod',
    top='hod',
    pathname='hod',
    provides=_doc('PROVIDES'),
    desc=_doc('SUMMARY'),
    longdesc=_doc('DESCRIPTION'),
    author=u'Andr\xe9 Malo',
    email='nd@perlig.de',
    url='http://opensource.perlig.de/hod/',
    classifiers=_lines(_doc('CLASSIFIERS') or ''),
    install_requires=_lines("""
        six >= 1.10.0
    """),
)


class build_ext(_build_ext.build_ext):  # pylint: disable = no-init
    """ Improved extension building code """

    def build_extension(self, ext):
        """
        Build C extension - with extended functionality

        The following features are added here:

        - The macros ``EXT_PACKAGE`` and ``EXT_MODULE`` will be filled (or
          unset) depending on the extensions name, but only if they are not
          already defined.

        - "." is added to the include directories (for cext.h)

        :Parameters:
          `ext` : `Extension`
            The extension to build

        :Return: whatever ``distutils.command.build_ext.build_ext`` returns
        :Rtype: any
        """
        # handle name macros
        macros = dict(ext.define_macros or ())
        tup = ext.name.split('.')
        if len(tup) == 1:
            pkg, mod = None, tup[0]
        else:
            pkg, mod = '.'.join(tup[:-1]), tup[-1]
        if pkg is not None and 'EXT_PACKAGE' not in macros:
            ext.define_macros.append(('EXT_PACKAGE', pkg))
        if 'EXT_MODULE' not in macros:
            ext.define_macros.append(('EXT_MODULE', mod))
        if pkg is None:
            macros = dict(ext.undef_macros or ())
            if 'EXT_PACKAGE' not in macros:
                ext.undef_macros.append('EXT_PACKAGE')

        if not ext.include_dirs:
            ext.include_dirs = ['.']
        elif '.' not in ext.include_dirs:
            ext.include_dirs.insert(0, '.')

        return _build_ext.build_ext.build_extension(self, ext)


EXTENSIONS = [
]


def setup():
    """ Main """
    with open('%(pathname)s/__init__.py' % package) as fp:
        for line in fp:  # pylint: disable = redefined-outer-name
            if line.startswith('__version__'):
                version = line.split('=', 1)[1].strip()
                if version.startswith(("'", '"')):
                    version = version[1:-1].strip()
                break
        else:
            raise RuntimeError("Version not found")

    packages = [package['top']] + [
        '%s.%s' % (package['top'], item)
        for item in
        _setuptools.find_packages(package['pathname'])
    ]

    _core.setup(
        cmdclass={'build_ext': build_ext},
        name=package['name'],
        author=package['author'],
        author_email=package['email'],
        classifiers=package['classifiers'],
        description=package['desc'],
        long_description=package['longdesc'],
        url=package['url'],
        ext_modules=EXTENSIONS,
        install_requires=package['install_requires'],
        packages=packages,
        version=version,
        zip_safe=False,
    )


if __name__ == '__main__':
    setup()
