#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-score',
    version='0.1.0a1',
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    maintainer='Dominik Gresch',
    maintainer_email='greschd@gmx.ch',
    license='GNU GPL v3.0',
    url='https://github.com/greschd/pytest-score',
    description='A plugin to run quality (non-binary) tests with pytest.',
    long_description=read('README.md'),
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=['pytest>=3.1.1', 'fsc.export', 'pyyaml'],
    extras_require={
        'dev': ['sphinx', 'pytest']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'score = pytest_score',
        ],
    },
)
