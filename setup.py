#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.1'
LONG_DESC = """\
Django Report Engine provides a reporting framework for Django 1.1+. Its goal is to be lightweight, provide multiple output formats, easily integrate into existing applications, and be open ended to both direct SQL reports, ORM based reports, or any other type of report imaginable. It is also attempting to be reasonably batteries-included with some basic Date based filtering assumptions, and simple namespacing of reports.

Reports are assumed to be tabular, with additional key/value "aggregates". A special form can be used to provide filtering/querying controls. There are premade filtering controls/framework to assist. Existing shortcut queryset and SQL based forms are integrated and can be quickly extended for generic reports. CSV, XML and HTML exports are included.
"""

setup(name='django-reportengine',
      version=VERSION,
      description="A Django app for building and integrating reports into your Django project.",
      long_description=LONG_DESC,
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='django reporting reports',
      maintainer = 'Nikolaj Baer',
      maintainer_email = 'nikolaj@cukerinteractive.com',
      url='http://github.com/cuker/django-reportengine',
      license='MIT License',
      packages=['reportengine'],
      zip_safe=False,
      install_requires=[
      ],
      test_suite='tests.runtests.runtests',
      )

