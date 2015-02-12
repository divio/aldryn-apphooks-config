# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from parler.managers import TranslatableManager, TranslatableQuerySet
except ImportError:
    raise ImportError(
        "Parler can not be found. Use pip install "
        "aldryn-apphooks-config[parler] or just install django-parler."
    )

from aldryn_apphooks_config.managers.base import (
    AppHookConfigQuerySet, AppHookConfigManager
)


class AppHookConfigTranslatableQueryset(AppHookConfigQuerySet,
                                        TranslatableQuerySet):
    pass


class AppHookConfigTranslatableManager(AppHookConfigManager,
                                       TranslatableManager):
    """
    Manager intended to use in TranslatableModels that has relations
    to apphooks configs. Add the namespace method to manager and queryset
    that should be used to filter objects by it namespace.
    """
    queryset_class = AppHookConfigTranslatableQueryset
    def get_queryset(self):
        return AppHookConfigTranslatableQueryset(self.model, using=self.db)
