# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.models import AppHookConfig
from aldryn_apphooks_config.utils import setup_config
from app_data import AppDataForm
from django import forms
from django.db import models


class ExampleConfig(AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    app_title = models.CharField('application title', max_length=234)


class AnotherExampleConfig(AppHookConfig):
    max_entries = models.SmallIntegerField(default=5)


@setup_config
class ExampleConfigForm(AppDataForm):
    model = ExampleConfig
    property = forms.CharField()
    published_default = forms.BooleanField(initial=True, required=False)


@setup_config
class AnotherExampleConfigForm(AppDataForm):
    model = AnotherExampleConfig
    property = forms.CharField()
