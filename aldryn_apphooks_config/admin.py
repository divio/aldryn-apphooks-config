# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import copy

from app_data.admin import AppDataModelAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from .utils import get_apphook_model


class BaseAppHookConfig(AppDataModelAdmin):
    """
    Base class for AppHookConfig admins

    The ModelAdmins for the AppHookConfig concrete models must:

    * Extends this class
    * Define a `get_config_fields` method that return a tuple of fields to be
      shown in the AppHookConfig fieldset. Every structure available in a single
      ModelAdmin fieldset `fields` definition can be returned by this method.
    """
    readonly_fields = ('type',)

    @property
    def declared_fieldsets(self):
        return [
            (None, {'fields': ('type', 'namespace')}),
            ('Config', {'fields': self.get_config_fields()})
        ]

    def get_config_fields(self):
        return ()


class ModelAppHookConfig(object):
    app_config_attribute = 'app_config'
    app_config_selection_title = u'Select app config'
    app_config_selection_desc = u'Select the app config for the new object'
    app_config_values = {}

    def _app_config_select(self, request, obj):
        """
        Return the select value for apphook configs

        :param request: request object
        :param obj: current object
        :return: False if no preselected value is available (more than one or no apphook
                 config is present), apphook config instance if exactly one apphook
                 config is defined or apphook config defined in the request or in the current
                 object, False otherwise
        """
        if not obj and not request.GET.get(self.app_config_attribute, False):
            config_model = get_apphook_model(self.model, self.app_config_attribute)
            if config_model.objects.count() == 1:
                return config_model.objects.first()
            return None
        elif obj and getattr(obj, self.app_config_attribute, False):
            return getattr(obj, self.app_config_attribute)
        elif request.GET.get(self.app_config_attribute, False):
            config_model = get_apphook_model(self.model, self.app_config_attribute)
            return config_model.objects.get(
                pk=int(request.GET.get(self.app_config_attribute, False))
            )
        return False

    def _set_config_defaults(self, request, form, obj=None):
        """
        Cycle through app_config_values and sets the form value according to the
        options in the current apphook config.

        self.app_config_values is a dictionary containing config options as keys, form fields as
        values::

            app_config_values = {
                'apphook_config': 'form_field',
                ...
            }

        :param request: request object
        :param form: model form for the current model
        :param obj: current object
        :return: form with defaults set
        """
        for config_option, field in self.app_config_values.items():
            if field in form.base_fields:
                form.base_fields[field].initial = self.get_config_data(request, obj, config_option)
        return form

    def get_fieldsets(self, request, obj=None):
        """
        If the apphook config must be selected first, returns a fieldset with just the
         app config field and help text
        :param request:
        :param obj:
        :return:
        """
        app_config_default = self._app_config_select(request, obj)
        if app_config_default is None and request.method == 'GET':
            return (_(self.app_config_selection_title),
                    {'fields': (self.app_config_attribute, ),
                     'description': _(self.app_config_selection_desc)}),
        else:
            return super(ModelAppHookConfig, self).get_fieldsets(request, obj)

    def get_config_data(self, request, obj, name):
        """
        Method that retrieves a configuration option for a specific AppHookConfig instance

        :param request: the request object
        :param obj: the model instance
        :param name: name of the config option as defined in the config form

        :return value: config value or None if no app config is found
        """
        return_value = None
        config = None
        if obj:
            try:
                config = getattr(obj, self.app_config_attribute, False)
            except ObjectDoesNotExist:  # pragma: no cover
                pass
        if not config and self.app_config_attribute in request.GET:
            config_model = get_apphook_model(self.model, self.app_config_attribute)
            try:
                config = config_model.objects.get(pk=request.GET[self.app_config_attribute])
            except config_model.DoesNotExist:  # pragma: no cover
                pass
        if config:
            return_value = getattr(config, name)
        return return_value

    def get_form(self, request, obj=None, **kwargs):
        """
        Provides a flexible way to get the right form according to the context

        For the add view it checks whether the app_config is set; if not, a special form
        to select the namespace is shown, which is reloaded after namespace selection.
        If only one namespace exists, the current is selected and the normal form
        is used.
        """
        form = super(ModelAppHookConfig, self).get_form(request, obj, **kwargs)
        if self.app_config_attribute not in form.base_fields:
            return form
        app_config_default = self._app_config_select(request, obj)
        if app_config_default:
            form.base_fields[self.app_config_attribute].initial = app_config_default
            get = copy.copy(request.GET)
            get[self.app_config_attribute] = app_config_default.pk
            request.GET = get
        elif app_config_default is None and request.method == 'GET':
            class InitialForm(form):
                class Meta(form.Meta):
                    fields = (self.app_config_attribute,)
            form = InitialForm
        form = self._set_config_defaults(request, form, obj)
        return form
