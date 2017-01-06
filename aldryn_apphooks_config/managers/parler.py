# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from aldryn_apphooks_config.managers.base import ManagerMixin, QuerySetMixin

try:
    from parler.managers import TranslatableManager, TranslatableQuerySet
except ImportError:  # pragma: no cover
    raise ImportError(
        'Parler can not be found. Use pip install '
        'aldryn-apphooks-config[parler] or just install django-parler.'
    )


class AppHookConfigTranslatableQueryset(TranslatableQuerySet, QuerySetMixin):

    def create(self, **kwargs):
        # Pass language setting to the object, as people start assuming
        # things like .language('xx').create(..) which is a nice API
        # after all.
        #
        # TODO: this create is copy of TranslatableQuerySet.create which
        # in someway is not called when using .language('en').create(..)
        # and instead is called Django Manager.create. I not figured why
        # it is acting like that.
        if self._language:
            kwargs['_current_language'] = self._language
        return super(TranslatableQuerySet, self).create(**kwargs)


class AppHookConfigTranslatableManager(TranslatableManager, ManagerMixin):
    """
    Manager intended to use in TranslatableModels that has relations
    to apphooks configs. Add the namespace method to manager and queryset
    that should be used to filter objects by it namespace.
    """
    queryset_class = AppHookConfigTranslatableQueryset

    def get_queryset(self):
        return self.queryset_class(self.model, using=self.db)
