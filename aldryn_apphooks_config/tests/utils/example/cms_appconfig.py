# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models

from aldryn_apphooks_config.models import AppHookConfig
from aldryn_apphooks_config.utils import setup_config
from app_data import AppDataForm


class ExampleConfig(AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    app_title = models.CharField(_('application title'), max_length=234)


class AnotherExampleConfig(AppHookConfig):
    max_entries = models.SmallIntegerField(default=5)


class ExampleConfigForm(AppDataForm):
    property = forms.CharField()
    published_default = forms.BooleanField(initial=True, required=False)
setup_config(ExampleConfigForm, ExampleConfig)


class AnotherExampleConfigForm(AppDataForm):
    property = forms.CharField()
setup_config(AnotherExampleConfigForm, AnotherExampleConfig)
