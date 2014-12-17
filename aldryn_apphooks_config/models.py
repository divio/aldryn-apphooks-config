# -*- coding: utf-8 -*-
from django.db import models


class AppHookConfigManager(models.Manager):
    def config(self, namespace):
        generic_config = self.get(namespace)
        config_class = load_model(self.get(namespace=namespace).type)
        return config_class.objects.get(pk=generic_config.pk)


@python_2_unicode_compatible
class AppHookConfig(models.Model):
    type = models.CharField()
    namespace = models.CharField()

    objects = AppHookConfigManager()

    class Meta:
        verbose_name = _(u'app-hook config')
        verbose_name_plural = _(u'app-hook configs')
        unique_together = ('type', 'namespace')

    def save(self, *args, **kwargs):
        self.type = '%s.%s' % (
            self.__class__.__module__, self.__class__.__name__)
        super(AppHookConfig, self).save(*args, **kwargs)

    def __str__(self):
        return _(u'%s / %s' % (self.type, self.namespace))