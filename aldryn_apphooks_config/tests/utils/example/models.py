# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_apphooks_config.managers import AppHookConfigManager
from aldryn_apphooks_config.managers.parler import AppHookConfigTranslatableManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from .cms_appconfig import AnotherExampleConfig, ExampleConfig


class Article(models.Model):
    title = models.CharField(_('title'), max_length=234)
    slug = models.SlugField()
    section = AppHookConfigField(ExampleConfig, verbose_name=_('section'))
    published = models.BooleanField(default=True, blank=True)

    objects = AppHookConfigManager()


class News(Article):
    config = AppHookConfigField(AnotherExampleConfig, verbose_name=_('config'))

    objects = AppHookConfigManager()


class TranslatableArticle(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField('title', max_length=234),
        slug=models.SlugField()
    )
    section = AppHookConfigField(ExampleConfig, verbose_name=_('section'))

    objects = AppHookConfigTranslatableManager()

class NotApphookedModel(models.Model):
    title = models.CharField(_('title'), max_length=234)
