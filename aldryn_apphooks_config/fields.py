# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .widgets import AppHookConfigWidget


class AppHookConfigFormField(forms.ModelChoiceField):

    def __init__(self, queryset, empty_label='---------',
                 required=True, widget=AppHookConfigWidget, *args, **kwargs):
        super(AppHookConfigFormField, self).__init__(
            queryset=queryset, empty_label=empty_label, required=required, widget=widget,
            *args, **kwargs
        )


class AppHookConfigField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs.update({'help_text': _('When selecting a value, the form is reloaded to '
                                      'get the updated default')})
        super(AppHookConfigField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({'form_class': AppHookConfigFormField})
        return super(AppHookConfigField, self).formfield(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^aldryn_apphooks_config\.fields\.AppHookConfigField'])
except:
    # If South isn't installed, then we didn't need this anyway.
    pass
