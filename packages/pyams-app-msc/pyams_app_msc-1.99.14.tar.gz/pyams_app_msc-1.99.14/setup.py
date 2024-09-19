#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""
This module contains PyAMS MSC application package
"""
import os
from setuptools import setup, find_packages


DOCS = os.path.join(os.path.dirname(__file__),
                    'docs')

README = os.path.join(DOCS, 'README.rst')
HISTORY = os.path.join(DOCS, 'HISTORY.rst')

version = '1.99.14'
long_description = open(README).read() + '\n\n' + open(HISTORY).read()

data_dir = 'pkg'
data_files = [(d, [os.path.join(d, f) for f in files])
              for d, folders, files in os.walk(data_dir)]

tests_require = [
    'pyams_content_themes',
    'pyramid_zcml',
    'zope.exceptions'
]

setup(name='pyams_app_msc',
      version=version,
      description="PyAMS application for cinema reservation management",
      long_description=long_description,
      classifiers=[
          "License :: OSI Approved :: Zope Public License",
          "Development Status :: 4 - Beta",
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Pyramid PyAMS',
      author='Thierry Florac',
      author_email='tflorac@ulthar.net',
      url='https://pyams.readthedocs.io',
      license='ZPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      package_data={
          '': ['*.rst', '*.txt', '*.pt',
               '*.pot', '*.po', '*.mo',
               '*.png', '*.gif', '*.jpeg', '*.jpg', '*.svg',
               '*.ttf', '*.woff2',
               '*.scss', '*.css', '*.js', '*.map']
      },
      data_files=data_files,
      zip_safe=False,
      python_requires='>=3.7',
      # uncomment this to be able to run tests with setup.py
      # test_suite="pyams_app_msc.tests.test_utilsdocs.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'colander',
          'cornice',
          'elasticsearch_dsl',
          'fanstatic',
          'hypatia',
          'persistent',
          'pillow',
          'pyams_catalog >= 2.1.0',
          'pyams_content >= 1.99.9',
          'pyams_content_api',
          'pyams_content_es',
          'pyams_file',
          'pyams_form >= 2.1.0',
          'pyams_i18n',
          'pyams_layer',
          'pyams_mail',
          'pyams_pagelet',
          'pyams_portal',
          'pyams_scheduler',
          'pyams_security >= 2.2.1',
          'pyams_security_views',
          'pyams_sequence',
          'pyams_site',
          'pyams_skin >= 2.2.3',
          'pyams_table',
          'pyams_utils >= 2.3.1',
          'pyams_viewlet',
          'pyams_workflow',
          'pyams_zmi >= 2.3.1',
          'pyams_zmq',
          'pyramid',
          'pyramid_mailer',
          'reportlab',
          'requests',
          'transaction',
          'ZODB',
          'zope.annotation',
          'zope.container',
          'zope.copy',
          'zope.dublincore',
          'zope.interface',
          'zope.intid',
          'zope.lifecycleevent',
          'zope.location',
          'zope.principalannotation',
          'zope.schema',
          'zope.traversing'
      ],
      entry_points={
          'fanstatic.libraries': [
              'msc = pyams_app_msc.zmi:library',
              'mscapp = pyams_app_msc.skin:library'
          ]
      })
