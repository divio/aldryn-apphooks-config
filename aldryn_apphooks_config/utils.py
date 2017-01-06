# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from app_data import AppDataContainer, app_registry
from cms.apphook_pool import apphook_pool
from django.core.urlresolvers import Resolver404, resolve
from django.db.models import ForeignKey
from django.utils.translation import get_language_from_request, override

# making key app/model specific to avoid inheritance issues
APP_CONFIG_FIELDS_KEY = '_app_config_field_names_{app_label}_{model_name}'


def get_app_instance(request):
    """
    Returns a tuple containing the current namespace and the AppHookConfig instance

    :param request: request object
    :return: namespace, config
    """
    app = None
    if getattr(request, 'current_page', None) and request.current_page.application_urls:
        app = apphook_pool.get_apphook(request.current_page.application_urls)

    if app and app.app_config:
        try:
            config = None
            with override(get_language_from_request(request, check_path=True)):
                namespace = resolve(request.path_info).namespace
                config = app.get_config(namespace)
            return namespace, config
        except Resolver404:
            pass
    return '', None


def setup_config(form_class, config_model):
    """
    Register the provided form as config form for the provided config model
    :param form_class: Form class derived from AppDataForm
    :param config_model: Model class derived from AppHookConfig
    :return:
    """
    app_registry.register('config', AppDataContainer.from_form(form_class), config_model)


def _get_apphook_field_names(model):
    """
    Return all foreign key field names for a AppHookConfig based model
    """
    from .models import AppHookConfig  # avoid circular dependencies
    fields = []
    for field in model._meta.fields:
        if isinstance(field, ForeignKey) and issubclass(field.rel.to, AppHookConfig):
            fields.append(field)
    return [field.name for field in fields]


def get_apphook_field_names(model):
    """
    Cache app-hook field names on model

    :param model: model class or object
    :return: list of foreign key field names to AppHookConfigs
    """
    key = APP_CONFIG_FIELDS_KEY.format(
        app_label=model._meta.app_label,
        model_name=model._meta.object_name
    ).lower()
    if not hasattr(model, key):
        field_names = _get_apphook_field_names(model)
        setattr(model, key, field_names)
    return getattr(model, key)


def get_apphook_configs(obj):
    """
    Get apphook configs for an object obj

    :param obj: any model instance
    :return: list of apphook configs for given obj
    """
    keys = get_apphook_field_names(obj)
    return [getattr(obj, key) for key in keys] if keys else []


def get_apphook_model(model, app_config_attribute):
    """
    Return the AppHookConfig model for the provided main model

    :param model: Main model
    :param app_config_attribute: Fieldname of the app_config
    :return: app_config model
    """
    return model._meta.get_field(app_config_attribute).rel.to
