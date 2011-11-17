#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

VERSION = '0.0.3'
LONG_DESC = """\
This package enables you to design forms in the Django admin.
These forms can be used in your code or to extend existing forms in the admin itself.
Other libraries may register new fields or widgets for the designer to use.
"""

setup(name='django-fieldmaker',
      version=VERSION,
      description="Dynamic form management in django",
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
      packages=find_packages(exclude=['test']),
      test_suite='tests.runtests.runtests',
      include_package_data = True,
      )
