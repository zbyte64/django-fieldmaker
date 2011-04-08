#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.0.1'
LONG_DESC = """\

"""

setup(name='django-fieldmaker',
      version=VERSION,
      description="",
      long_description=LONG_DESC,
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='django',
      maintainer = 'Jason Kraus',
      maintainer_email = 'zbyte64@gmail.com',
      url='http://github.com/cuker/',
      license='New BSD License',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      zip_safe=True,
      install_requires=[
      ],
      test_suite='tests.runtests.runtests',
      )
