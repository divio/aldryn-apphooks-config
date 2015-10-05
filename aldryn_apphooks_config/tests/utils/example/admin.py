# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.admin import BaseAppHookConfig, ModelAppHookConfig
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from django.contrib import admin

from .models import Article, ExampleConfig


class ArticleAdmin(FrontendEditableAdminMixin,
                   ModelAppHookConfig,
                   admin.ModelAdmin):
    list_display = ('title', 'section', 'slug')
    app_config_attribute = 'section'
    app_config_selection_title = u'Select app config'
    app_config_selection_desc = u'Select the app config for the new object'
    app_config_values = {
        'published_default': 'published'
    }

admin.site.register(Article, ArticleAdmin)


class ExampleConfigAdmin(BaseAppHookConfig):
    def get_config_fields(self):
        return ['config.property', 'config.published_default']

admin.site.register(ExampleConfig, ExampleConfigAdmin)
