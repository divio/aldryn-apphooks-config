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
    if kwargs:
        return urlresolvers.reverse(
            'example:{0:s}'.format(view_name),
            kwargs=kwargs, current_app=namespace)
    elif args:
        return urlresolvers.reverse(
            'example:{0:s}'.format(view_name),
            args=args, current_app=namespace)
    else:
        return urlresolvers.reverse(
            'example:{0:s}'.format(view_name), current_app=namespace)
