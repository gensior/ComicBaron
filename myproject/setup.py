#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='comicbaron',
      version='0.1',
      packages=find_packages(),
      package_data={'comicbaron': ['bin/*.*', 'static/*.*', 'templates/*.*']},
      exclude_package_data={'comicbaron': ['bin/*.pyc']},
      scripts=['comicbaron/bin/manage.py'])
