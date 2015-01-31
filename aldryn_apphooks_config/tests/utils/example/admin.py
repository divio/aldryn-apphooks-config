# -*- coding: utf-8 -*-
from aldryn_apphooks_config.admin import BaseAppHookConfig
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from django.contrib import admin

from .models import Article, ExampleConfig


class ArticleAdmin(FrontendEditableAdminMixin,
                   admin.ModelAdmin):
    list_display = ('title', 'section', 'slug')

admin.site.register(Article, ArticleAdmin)


class ExampleConfigAdmin(BaseAppHookConfig):
    def get_config_fields(self):
        return ['config.property']

admin.site.register(ExampleConfig, ExampleConfigAdmin)
