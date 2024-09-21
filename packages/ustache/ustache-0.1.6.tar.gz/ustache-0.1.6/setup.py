"""ustache setuptools script."""
"""
ustache, mstache wrapper, Mustache for Python
=============================================

This project has been renamed to **mstache**, refer to the new
`mstache README.md`_ and `mstache repository`_.

See also `README.md`_, `project documentation`_ and `project repository`_.

.. _mstache README.md: https://mstache.readthedocs.io/en/latest/README.html
.. _mstache repository: https://gitlab.com/ergoithz/mstache
.. _README.md: https://ustache.readthedocs.io/en/latest/README.html
.. _project documentation: https://ustache.readthedocs.io
.. _project repository: https://gitlab.com/ergoithz/ustache


License
-------

Copyright (c) 2021-2024, Felipe A Hernandez.

MIT License (see `LICENSE`_).

.. _LICENSE: https://gitlab.com/ergoithz/ustache/-/blob/master/LICENSE

"""

import datetime
import os
import pathlib
import re

from setuptools import setup

repository = 'https://gitlab.com/ergoithz/ustache'
readme = re.sub(
    r'(?P<prefix>!?)\[(?P<text>[^]]+)\]\(\./(?P<src>[^)]+)\)',
    lambda match: (
        '{prefix}[{text}]({repository}/-/{view}/master/{src})'.format(
            repository=repository,
            view='raw' if match.group('prefix') == '!' else 'blob',
            **match.groupdict(),
            )),
    pathlib.Path('README.md').read_text(),
    )
__author__, __email__, __license__, __version__ = (
    re.search(
        rf"__{name}__ = '([^']+)'",
        pathlib.Path('ustache.py').read_text(),
        ).group(1)
    for name in ('author', 'email', 'license', 'version')
    )
version = (
    __version__
    if os.getenv('TWINE_REPOSITORY') == 'pypi' else
    '{}a{}'.format(__version__, datetime.date.today().strftime('%Y%m%d'))
    )
setup(
    name='ustache',
    version=version,
    url=repository,
    license=__license__,
    author=__author__,
    author_email=__email__,
    description='ustache, Mustache for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        ],
    python_requires='>=3.10.0',
    install_requires=[
        'mstache==0.2.0',
        ],
    extras_require={
        'optional': [
            'xxhash>=1.2.0',
            ],
        'codestyle': [
            'flake8',
            'flake8-blind-except',
            'flake8-bugbear',
            'flake8-builtins',
            'flake8-commas',
            'flake8-docstrings',
            'flake8-import-order',
            'flake8-logging-format',
            'flake8-rst-docstrings',
            'flake8-simplify',
            'mypy',
            ],
        'coverage': [
            'coverage',
            ],
        'docs': [
            'recommonmark',
            'sphinx',
            'sphinx-autodoc-typehints',
            ],
        'release': [
            'wheel',
            'twine',
            ],
        'tests': [
            'coverage',
            'xxhash',
            ],
        'benchmark': [
            'chevron',
            ],
        },
    keywords=['template', 'mustache'],
    py_modules=['ustache'],
    test_suite='tests',
    platforms='any',
    zip_safe=True,
    )
