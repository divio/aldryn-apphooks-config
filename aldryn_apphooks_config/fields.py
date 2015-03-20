# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .widgets import AppHookConfigWidget


class AppHookConfigField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs.update({'help_text': _(u'When selecting a value, the form is reloaded to get the updated default')})
        super(AppHookConfigField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        class AppHookConfigFormField(forms.ModelChoiceField):
            widget = AppHookConfigWidget
        kwargs.update({'form_class': AppHookConfigFormField})
        return super(AppHookConfigField, self).formfield(**kwargs)
