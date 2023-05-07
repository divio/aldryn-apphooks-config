Changelog
=========


0.7.0 (2023-05-07)
==================

* Add Django 3.2+ support

0.6.0 (2020-05-12)
==================

* Add Django 3.0 support

0.5.3 (2019-10-19)
==================

* Fix media asset declaration on django 2.2+

0.5.2 (2019-01-02)
==================

* Changed deprecated ``rel.to`` to ``remote_field.model``
* Fixed migration for example app
* Fixed issues for Django 2.0 and up


0.5.1 (2018-12-18)
==================

* Added support for Django 2.0 and 2.1
* Removed support for Django < 1.11
* Adapted testing infrastructure (tox/travis) to incorporate django CMS 3.6
* Fixed setup.py


0.4.2 (2018-12-17)
==================

* Fixed issue with Django 1.10 and below in AppHookConfigWidget


0.4.1 (2018-04-10)
==================

* django-appdata>=0.2.0 is now required


0.4.0 (2018-03-19)
==================

* Added Django 1.11 compatibility
* Added django CMS 3.5 compatibility
* Implemented django-appdata 0.2 interface
* Removed south migrations
* Dropped support for django CMS 3.3 and below
* Allowed use setup_config as decorators


0.3.3 (2017-03-06)
==================

* Fixed MANIFEST.in typo


0.3.2 (2017-03-06)
==================

* Fixed setup.py issue
* Added locale files to MANIFEST.in


0.3.1 (2017-03-02)
==================

* Added translation system
* Added german translation


0.3.0 (2017-01-06)
==================

* Allowed override AppHookConfigField attributes
* Dropped Django 1.7 and below
* Dropped django CMS 3.1 and below
* Added Django 1.10 support


0.2.7 (2016-03-03)
==================

* Set namespace as readonly
* Added official Django 1.9 support
* Updated readme
* Used path_info instead of path in resolve


0.2.6 (2015-10-05)
==================

* Added support for Python 3.5
* Added support for Django 1.9a1
* Code style cleanup and tests


0.2.5 (2015-09-25)
==================

* Added support for Django 1.8, django CMS 3.2
* AppHookConfigTranslatableManager.get_queryset should use queryset_class
* Skipped overriding admin form if app_config field not present


0.2.4 (2015-04-20)
==================

* Fixed issue where an apphook could not be changed, once set.
* Added optional 'default' kwarg to namespace_url templatetag


0.1.0 (2014-01-01)
==================

* Released first version on PyPI.
