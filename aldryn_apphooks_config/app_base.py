# -*- coding: utf-8 -*-


class CMSConfigApp(object):
    name = None
    urls = None
    menus = []
    app_name = None
    app_config = None
    permissions = True
    exclude_permissions = []

    def get_config(self, namespace):
        return self.app_config.objects.get(namespace=namespace)