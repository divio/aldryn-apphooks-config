from setuptools import find_packages, setup

from aldryn_apphooks_config import __version__

REQUIREMENTS = [
    'django-appdata>=0.2.0',
    'django-cms>=3.4.5'
],


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
],


setup(
    name='aldryn-apphooks-config',
    version=__version__,
    description='Namespaces based configuration for Apphooks',
    long_description=open('README.rst').read(),
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/aldryn/aldryn-apphooks-config',
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    keywords='aldryn-apphooks-config',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
