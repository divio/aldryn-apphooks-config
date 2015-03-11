# -*- coding: utf-8 -*-

from django import template
from django.core import urlresolvers

from ..utils import get_app_instance


register = template.Library()


@register.simple_tag(takes_context=True)
def namespace_url(context, view_name, *args, **kwargs):
    """
    Returns an absolute URL matching given view with its parameters.
    """

    namespace, config = get_app_instance(context['request'])
    if not 'current_app' in kwargs:
        kwargs['current_app'] = namespace

    return urlresolvers.reverse('%s:%s' % (config.namespace, view_name),
                                args=args,
                                kwargs=kwargs)
