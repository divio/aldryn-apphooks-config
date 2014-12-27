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

    djangocms-helper aldryn_apphooks_config server --cms --extra-settings=test_settings

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


Features
--------

* TODO