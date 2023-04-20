from cms.app_base import CMSApp
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


class CMSConfigApp(CMSApp):
    def get_configs(self):
        return self.app_config.objects.all()

    def get_config(self, namespace):
        try:
            return self.app_config.objects.get(namespace=namespace)
        except ObjectDoesNotExist:
            return None

    def get_config_add_url(self):
        try:
            return reverse("admin:{}_{}_add".format(self.app_config._meta.app_label, self.app_config._meta.model_name))
        except AttributeError:  # pragma: no cover
            return reverse(
                "admin:{}_{}_add".format(self.app_config._meta.app_label, self.app_config._meta.module_name)
            )
