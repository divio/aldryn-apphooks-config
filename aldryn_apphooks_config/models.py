# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from app_data import AppDataField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class AppHookConfig(models.Model):
    """
    This is the generic (abstract) model that holds the configurations for each AppHookConfig
    concrete model
    """
    type = models.CharField(_('type'), max_length=100)
    namespace = models.CharField(
        _(u'instance namespace'), default=None, max_length=100, unique=True)
    app_data = AppDataField()

    cmsapp = None

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
        if self.cmsapp:
            return _(u'%s / %s') % (self.cmsapp.name, self.namespace)
        else:
            return _(u'%s / %s') % (self.type, self.namespace)

    def __getattr__(self, item):
        """
        This allows to access config form attribute as normal model fields

        :param item:
        :return:
        """
        try:
            return getattr(self.app_data.config, item)
        except:
            raise AttributeError('attribute %s not found' % item)
