# -*- coding: utf-8 -*-

from django import template
from django.core import urlresolvers

from ..utils import get_app_instance


register = template.Library()


@register.simple_tag(takes_context=True)
def namespace_url(context, view_name, *args, **kwargs):
    """
    Returns an absolute URL matching named view with its parameters and the
    provided application instance namespace. If no namespace is passed as a
    kwarg (or it is "" or None), this templatetag will look into the request
    object for the app_config's namespace. If there is still no namespace found,
    this tag will act like the normal {% url ... %} tag.
    """

    namespace = kwargs.pop('namespace', None)

    if not namespace:
        namespace, __ = get_app_instance(context['request'])

    if namespace:
        namespace += ":"

    if kwargs:
        return urlresolvers.reverse(
            '{0:s}{1:s}'.format(namespace, view_name),
            kwargs=kwargs)
    elif args:
        return urlresolvers.reverse(
            '{0:s}{1:s}'.format(namespace, view_name),
            args=args)
    else:
        return urlresolvers.reverse(
            '{0:s}{1:s}'.format(namespace, view_name))
