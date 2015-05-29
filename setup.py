#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

setup(name='hiparser',
      version='1.0',
      description='Script that emulates parsing chat commands.',
      long_description=read('README.md'),
      author='Corwin Brown',
      author_email='corwin@corwinbrown.com',
      packages=['hiparser', 'tests'],
      install_requires=['BeautifulSoup==3.2.1', 'wsgiref==0.1.2'],
      test_suite='tests.test_hiparser.HiparserTests',
      plaform='all')
