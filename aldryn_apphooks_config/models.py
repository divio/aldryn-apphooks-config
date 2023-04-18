from app_data import AppDataField
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppHookConfig(models.Model):
    """
    This is the generic (abstract) model that holds the configurations for each AppHookConfig
    concrete model
    """

    type = models.CharField(
        _("Type"),
        max_length=100,
    )
    namespace = models.CharField(
        _("Instance namespace"),
        default=None,
        max_length=100,
        unique=True,
    )
    app_data = AppDataField()

    cmsapp = None

    class Meta:
        verbose_name = _("Apphook config")
        verbose_name_plural = _("Apphook configs")
        unique_together = ("type", "namespace")
        abstract = True

    def save(self, *args, **kwargs):
        self.type = "{}.{}".format(self.__class__.__module__, self.__class__.__name__)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.cmsapp:
            return "{} / {}".format(self.cmsapp.name, self.namespace)
        else:
            return "{} / {}".format(self.type, self.namespace)

    def __getattr__(self, item):
        """
        This allows to access config form attribute as normal model fields

        :param item:
        :return:
        """
        try:
            return getattr(self.app_data.config, item)
        except Exception:
            raise AttributeError("attribute %s not found" % item)
