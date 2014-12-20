# -*- coding: utf-8 -*-
from app_data.admin import AppDataModelAdmin


class BaseAppHookConfig(AppDataModelAdmin):
    """
    Base class for AppHookConfig admins

    The ModelAdmins for the AppHookConfig concrete models must:

    * Extends this class
    * Define a `get_config_fields` method that return a tuple of fields to be
      shown in the AppHookConfig fieldset. Every structure available in a single
      ModelAdmin fieldset `fields` definition can be returned by this method.
    """
    readonly_fields = ('type',)

    @property
    def declared_fieldsets(self):
        return [
            (None, {'fields': ('type', 'namespace')}),
            ('Config', {'fields': self.get_config_fields()})
        ]

    def get_config_fields(self):
        return ()