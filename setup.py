#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import aldryn_apphooks_config

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = aldryn_apphooks_config.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m \'version %s\'' % (version, version))
    print('  git push --tags')
    sys.exit()

readme = open('README.rst').read()
history = open('CHANGELOG.rst').read().replace('.. :changelog:', '')

setup(
    name='aldryn-apphooks-config',
    version=version,
    description='''Namespaces based configuration for Apphooks''',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/aldryn/aldryn-apphooks-config',
    packages=[
        'aldryn_apphooks_config',
    ],
    include_package_data=True,
    install_requires=[
        'django-appdata>=0.1.6',
        'django-cms>=3.4'
    ],
    extra_requires={
        'parler': 'django-parler>=1.4'
    },
    test_suite='test_settings.run',
    license='BSD',
    zip_safe=False,
    keywords='aldryn-apphooks-config',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
