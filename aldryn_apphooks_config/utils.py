# -*- coding: utf-8 -*-
from app_data import AppDataContainer, app_registry
from cms.apphook_pool import apphook_pool
from django.core.urlresolvers import resolve


def get_app_instance(request):
    """
    Returns a tuple containing the current namespace and the AppHookConfig instance

    :param request: request object
    :return: namespace, config
    """
    app = None
    if getattr(request, 'current_page', None):
        app = apphook_pool.get_apphook(request.current_page.application_urls)

    config = None
    namespace = resolve(request.path_info).namespace
    if app and app.app_config:
        config = app.get_config(namespace)
    return namespace, config


def setup_config(form_class, config_model):
    """
    Register the provided form as config form for the provided config model
    :param form_class: Form class derived from AppDataForm
    :param config_model: Model class derived from AppHookConfig
    :return:
    """
    app_registry.register('config', AppDataContainer.from_form(form_class), config_model)