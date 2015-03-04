# -*- coding: utf-8 -*-
from app_data import AppDataField
from django.core.exceptions import ObjectDoesNotExist
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

    @classmethod
    def get_config_data(cls, request, name, obj, config_attribute, config_default=None):
        """
        Static method that retrieves a configuration option for a specific AppHookConfig instance

        This is mostly meant to be used in the ModelAdmin get_form method:

            config_option = MyAppHookConfigModel.get_config_data(
                request, 'my_option', obj, 'app_config',
                getattr(settings, 'SOME_FALLBACK_DEFAULT', True))

            form = super(MyModelAdmin, self).get_form(request, obj, **kwargs)
            form.base_fields['a_field'].initial = config_option


        :param request: the request object
        :param name: name of the config option as defined in the config form
        :param obj: the model instance
        :param config_attribute: name of the AppHookConfig attribute in the model
        :param config_default: default value (if any) for the given config option, if no default
                               is provided by the AppHookConfigModel
        """
        return_value = None
        config = None
        if obj:
            try:
                config = getattr(obj, config_attribute, False)
            except ObjectDoesNotExist:
                pass
        if not config and config_attribute in request.GET:
            try:
                config = cls.objects.get(pk=request.GET[config_attribute])
            except cls.DoesNotExist:
                pass
        if config:
            return_value = getattr(config, name)
        if return_value is None and config_default is not None:
            return config_default
        return return_value