# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from cms.app_base import CMSApp


class CMSConfigApp(CMSApp):

    def get_configs(self):
        return self.app_config.objects.all()

    def get_config(self, namespace):
        return self.app_config.objects.get(namespace=namespace)

    def get_config_add_url(self):
        return reverse('admin:%s_%s_add' % (self.app_config._meta.app_label,
                                            self.app_config._meta.model_name))