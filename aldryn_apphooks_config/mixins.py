# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


def AppConfigMixin(object):
    def dispatch(self, *args, **kwargs)
        self.namespace = resolve(self.request.path).namespace
        self.config = get_app_config(resolve(self.request.path).namespace)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = self.namespace
        return super(BasePostView, self).render_to_response(context,
                                                            **response_kwargs)