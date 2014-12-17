# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


def get_app_config(namespace):
    return config.objects.get(namespace=namespace)