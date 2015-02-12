# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.managers import ApphooksConfigManager
from .config import ExampleConfig, AnotherExampleConfig


class Article(models.Model):
    title = models.CharField(_('title'), max_length=234)
    slug = models.SlugField()
    section = models.ForeignKey(ExampleConfig, verbose_name=_('section'))

    objects = ApphooksConfigManager()


class News(Article):
    config = models.ForeignKey(AnotherExampleConfig, verbose_name=_('config'))

    objects = ApphooksConfigManager()
