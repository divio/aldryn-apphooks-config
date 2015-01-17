=============================
aldryn-apphooks-config
=============================

.. image:: https://badge.fury.io/py/aldryn-apphooks-config.png
    :target: https://badge.fury.io/py/aldryn-apphooks-config

.. image:: https://travis-ci.org/aldryn/aldryn-apphooks-config.png?branch=master
    :target: https://travis-ci.org/aldryn/aldryn-apphooks-config

.. image:: https://coveralls.io/repos/aldryn/aldryn-apphooks-config/badge.png?branch=master
    :target: https://coveralls.io/r/aldryn/aldryn-apphooks-config?branch=master

Namespaces based configuration for app-hooks

Quickstart
----------

To start testing namespace configuration::

    pip install https://github.com/aldryn/aldryn-apphooks-config/archive/master.zip

The application defines a runnable testing configuration to experiment with it:

Install dependencies::

    pip install -r requirements-test.txt

Run using djangocms-helper::

    python test_settings.py server --cms

Then:

* go to http://localhost:8000
* create an home page
* create a child page
* go to the advanced settings
* select "NewsBlog" application
* an empty "Application configurations" appears
* click on the "+" icon and define an application configuration
* the newly created configuration is selected in the dropdown
* save and publish the page
* go to "Aldryn_Newsblog" -> "Articles" -> "Add article"
* fill in with the requested data; from the "namespace" dropdown select the above configuration
* save
* profit!

Implement support for apphooks configuration
--------------------------------------------

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


Implementation step-guide
=========================

* Define a AppHookConfig model::

    from aldryn_apphooks_config.models import AppHookConfig

    class NewsBlogConfig(AppHookConfig):
        pass

  Implementation can be completely empty as the schema is defined in the
  parent (abstract) model

* Define a ConfigForm::

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

* Define an admin class for the AppHookConfig model::

    from django.contrib import admin
    from aldryn_apphooks_config.admin import BaseAppHookConfig

    class BlogConfigAdmin(BaseAppHookConfig):

        def get_config_fields(self):
            # this method **must** be implemented and **must** return the
            # fields defined in the above form, with the ``config`` prefix
            # This is dependent on the django-appdata API
            return ('config.show_authors', ...)

* Define a CMSApp derived from CMSConfigApp provided by this application::

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
            return Article.objects.filter(namespace__namespace=self.namespace)

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


Features
--------

* TODO