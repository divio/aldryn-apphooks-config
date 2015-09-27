# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from .utils import get_app_instance


class AppConfigMixin(object):
    """
    This mixin must be attached to any class-based views used which implements AppHookConfig.

    It provides:
    * current namespace in self.namespace
    * namespace configuration in self.config
    * current application in the `current_app` context variable
    """
    def dispatch(self, request, *args, **kwargs):
        self.namespace, self.config = get_app_instance(request)
        return super(AppConfigMixin, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = self.namespace
        return super(AppConfigMixin, self).render_to_response(context, **response_kwargs)
