#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='twentyfive',
    version='0.2.dev1',
    description='State machine suitable for long-running systems',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='http://github.com/mbr/twentyfive',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    extras_require={
        'tools': ['click', 'pygraphviz'],
    },
    entry_points={
        'console_scripts': [
            'sm25 = twentyfive.cli:cli [tools]',
        ]
    }
)
