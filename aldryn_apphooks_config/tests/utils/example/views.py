# -*- coding: utf-8 -*-
from aldryn_apphooks_config.mixins import AppConfigMixin
from django.views.generic import ListView, DetailView

from .models import Article


class ArticleDetail(AppConfigMixin, DetailView):
    model = Article
    slug_field = 'slug'

    def get_template_names(self):
        return '%s/article_detail.html' % self.config.namespace


class ArticleList(AppConfigMixin, ListView):
    """A complete list of articles."""
    model = Article

    def get_template_names(self):
        return '%s/article_list.html' % self.config.namespace

    def get_queryset(self):
        return Article.objects.all().filter(
            section__namespace=self.namespace
        )
