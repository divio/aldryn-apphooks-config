# -*- coding: utf-8 -*-
from app_data import AppDataField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AppHookConfig(models.Model):
    """
    This is the generic (abstract) model that holds the configurations for each AppHookConfig
    concrete model
    """
    type = models.CharField(_('type'), max_length=100)
    namespace = models.CharField(_(u'instance namespace'), default=None, max_length=100)
    app_data = AppDataField()

    class Meta:
        verbose_name = _(u'Apphook config')
        verbose_name_plural = _(u'Apphook configs')
        unique_together = ('type', 'namespace')
        abstract = True

    def save(self, *args, **kwargs):
        self.type = '%s.%s' % (
            self.__class__.__module__, self.__class__.__name__)
        super(AppHookConfig, self).save(*args, **kwargs)

    def __str__(self):
        return _(u'%s / %s') % (self.type, self.namespace)