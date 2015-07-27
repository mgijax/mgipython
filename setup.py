#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup(name='MgiPython',
      version='0.1',
      description='MGI Python Libraries and APIs',
      author='MGI Software Group',
      packages=find_packages(exclude=['tests*']),
      install_requires=[
            'psycopg2',
            'sqlalchemy',
            'Flask',
            'Flask-SQLAlchemy',
            'flask_login',
            'wtforms',
            'cherrypy'
      ]
     )
