# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .config import ExampleConfig


class Article(models.Model):
    title = models.CharField(_('title'), max_length=234)
    slug = models.SlugField()
    section = models.ForeignKey(ExampleConfig, verbose_name=_('section'))

