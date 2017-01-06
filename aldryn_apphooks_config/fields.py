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
        if 'help_text' not in kwargs:
            kwargs.update({'help_text': _('When selecting a value, the form is reloaded to '
                                          'get the updated default')})
        super(AppHookConfigField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if 'form_class' not in kwargs:
            kwargs.update({'form_class': AppHookConfigFormField})
        return super(AppHookConfigField, self).formfield(**kwargs)
