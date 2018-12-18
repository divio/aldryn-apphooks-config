|PyPI Version| |Build Status| |Coverage Status|

======================
aldryn-apphooks-config
======================

Namespaces based configuration for Apphooks

Basic concepts
==============

The concept of apphooks-config is to store all the configuration
in an applications-specific model, and let the developer
specify the desired option in a form.
In the views the model instance specific for the current
application namespace is loaded (through a mixin) and it's
thus available in the view to provide the configuration for
the current namespace.

Namespaces can be created on the fly in the ``Page`` admin
**Advanced settings** by following the steps above.
When creating an application configuration, you are in fact defining a
namespace, which is saved in the same field in the ``Page`` model as the
plain namespaces.


Contributing
------------

We're grateful to all contributors who have helped create and maintain this package.

Contributors are listed at `contributions page
<https://github.com/divio/djangocms-video/graphs/contributors>`_.


Supported django CMS versions
-----------------------------

+----------------+-------+-------+-------+-------+
|                | 0.2.x | 0.3.x | 0.4.x | 0.5.x |
+----------------+-------+-------+-------+-------+
| django CMS 3.1 |   ✔   |   ✗   |   ✗   |   ✗   |
+----------------+-------+-------+-------+-------+
| django CMS 3.2 |   ✔   |   ✔   |   ✗   |   ✗   |
+----------------+-------+-------+-------+-------+
| django CMS 3.3 |   ✗   |   ✔   |   ✗   |   ✗   |
+----------------+-------+-------+-------+-------+
| django CMS 3.4 |   ✗   |   ✔   |   ✔   |   ✔   |
+----------------+-------+-------+-------+-------+
| django CMS 3.5 |   ✗   |   ✗   |   ✔   |   ✔   |
+----------------+-------+-------+-------+-------+
| django CMS 3.6 |   ✗   |   ✗   |   ✔   |   ✔   |
+----------------+-------+-------+-------+-------+

Supported Django versions
-------------------------

+----------------+-------+-------+-------+-------+
|                | 0.2.x | 0.3.x | 0.4.x | 0.5.x |
+----------------+-------+-------+-------+-------+
| django 1.6     |   ✔   |   ✗   |   ✗   |   ✗   |
+----------------+-------+-------+-------+-------+
| django 1.7     |   ✔   |   ✗   |   ✗   |   ✗   |
+----------------+-------+-------+-------+-------+
| django 1.8     |   ✔   |   ✔   |   ✔   |   ✗   |
+----------------+-------+-------+-------+-------+
| django 1.9     |   ✔   |   ✔   |   ✔   |   ✗   |
+----------------+-------+-------+-------+-------+
| django 1.10    |   ✗   |   ✔   |   ✔   |   ✗   |
+----------------+-------+-------+-------+-------+
| django 1.11    |   ✗   |   ✔   |   ✔   |   ✔   |
+----------------+-------+-------+-------+-------+
| django 2.0     |   ✗   |   ✗   |   ✗   |   ✔   |
+----------------+-------+-------+-------+-------+
| django 2.1     |   ✗   |   ✗   |   ✗   |   ✔   |
+----------------+-------+-------+-------+-------+


Implementation step-guide
=========================

* Define a AppHookConfig model in ``cms_appconfig.py``::

    from aldryn_apphooks_config.models import AppHookConfig

    class NewsBlogConfig(AppHookConfig):
        pass

  Implementation can be completely empty as the schema is defined in the
  parent (abstract) model

* Use apphooks managers in your model::

    from aldryn_apphooks_config.managers import AppHookConfigManager

    class Article(models.Model):
        title = models.CharField()

        objects = AppHookConfigManager()

``AppHookConfigManager`` adds ``namespace`` method to manager and queryset::

    Article.objects.namespace('foobar')

There is also a proper queryset, the ``ApphooksConfigQueryset``. Parler
integrated variants can be found in ``aldryn_apphooks_config.managers.parler``.
Names are ``AppHookConfigTranslatableManager`` and
``AppHookConfigTranslatableQueryset``.

* Define a ConfigForm in ``cms_appconfig.py``::

    from app_data import AppDataForm
    from django import forms
    from aldryn_newsblog.models import NewsBlogConfig
    from aldryn_apphooks_config.utils import setup_config

    class BlogOptionForm(AppDataForm):
        # fields are totally arbitrary: any form field supported by
        # django-appdata is supported
        show_authors = forms.BooleanField(required=False)
        ...

    # this function will register the provided form with the model created
    # at the above step
    setup_config(BlogOptionForm, NewsBlogConfig)

    # setup_config can be used as a decorator too, but the `model`
    # attribute must be added to the form class
    @setup_config
    class BlogOptionForm(AppDataForm):
        model = NewsBlogConfig




* Define an admin class for the AppHookConfig model (usually in ``admin.py``::

    from django.contrib import admin
    from aldryn_apphooks_config.admin import BaseAppHookConfig

    class BlogConfigAdmin(BaseAppHookConfig):

        def get_config_fields(self):
            # this method **must** be implemented and **must** return the
            # fields defined in the above form, with the ``config`` prefix
            # This is dependent on the django-appdata API
            return ('config.show_authors', ...)

* Define a CMSApp derived from CMSConfigApp provided by this application
(in ``cms_app.py``/``cms_apps.py``)::

    from aldryn_apphooks_config.app_base import CMSConfigApp
    from cms.apphook_pool import apphook_pool
    from django.utils.translation import ugettext_lazy as _
    from .models import NewsBlogConfig


    class NewsBlogApp(CMSConfigApp):
        name = _('NewsBlogApp')
        urls = ['aldryn_newsblog.urls']
        app_name = 'aldryn_newsblog'
        # this option is specific of CMSConfigApp, and links the
        # CMSApp to a specific AppHookConfig model
        app_config = NewsBlogConfig

    apphook_pool.register(NewsBlogApp)

* Implements your views inheriting the ``AppConfigMixin``::

    from django.views.generic.detail import DetailView
    from aldryn_apphooks_config.mixins import AppConfigMixin

    class ArticleDetail(AppConfigMixin, DetailView):
        def get_queryset(self):
            return Article.objects.namespace(self.namespace)

  ``AppConfigMixin`` provides a complete support to namespaces, so the view
  is not required to set anything specific to support them; the following
  attributes are set for the view class instance:

  * current namespace in ``self.namespace``
  * namespace configuration (the instance of NewsBlogConfig) in ``self.config``
  * current application in the ``current_app`` parameter passed to the
    Response class

Test setup
==========

To properly setup the data for tests to run for a apphook-config enabled application,
make sure you add the following code to your TestCase::

    MyTestCase():

        def setUp(self):
            # This is the namespace represented by the AppHookConfig model instance
            self.ns_newsblog = NewsBlogConfig.objects.create(namespace='NBNS')
            self.page = api.create_page(
                'page', self.template, self.language, published=True,
                # this is the name of the apphook defined in the CMSApp class
                apphook='NewsBlogApp',
                # The namespace is the namespace field of the AppHookConfig instance created above
                apphook_namespace=self.ns_newsblog.namespace)
            # publish the page to make the apphook available
            self.page.publish(self.language)


.. |PyPI Version| image:: http://img.shields.io/pypi/v/aldryn-apphooks-config.svg
   :target: https://pypi.python.org/pypi/aldryn-apphooks-config
.. |Build Status| image:: http://img.shields.io/travis/aldryn/aldryn-apphooks-config/master.svg
   :target: https://travis-ci.org/aldryn/aldryn-apphooks-config
.. |Coverage Status| image:: http://img.shields.io/coveralls/aldryn/aldryn-apphooks-config/master.svg
   :target: https://coveralls.io/r/aldryn/aldryn-apphooks-config?branch=master
