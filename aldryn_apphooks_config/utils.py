# -*- coding: utf-8 -*-
from app_data import AppDataContainer, app_registry
from django.db.models import ForeignKey
from cms.apphook_pool import apphook_pool
from django.core.urlresolvers import resolve, Resolver404


def get_app_instance(request):
    """
    Returns a tuple containing the current namespace and the AppHookConfig instance

    :param request: request object
    :return: namespace, config
    """
    app = None
    if getattr(request, 'current_page', None):
        app = apphook_pool.get_apphook(request.current_page.application_urls)

    if app and app.app_config:
        try:
            config = None
            namespace = resolve(request.path).namespace
            if app and app.app_config:
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


def get_apphook_field_names(model):
    """
    Return all foreign key field names for a AppHookConfig based model
    """
    from .models import AppHookConfig  # avoid circular dependencies
    fields = []
    for field in model._meta.fields:
        if (isinstance(field, ForeignKey)
                and issubclass(field.rel.to, AppHookConfig)):
            fields.append(field)
    return [field.name for field in fields]


def get_apphook_model(model, app_config_attribute):
    """
    Return the AppHookConfig model for the provided main model

    :param model: Main model
    :param app_config_attribute: Fieldname of the app_config
    :return: app_config model
    """
    return model._meta.get_field_by_name(app_config_attribute)[0].rel.to