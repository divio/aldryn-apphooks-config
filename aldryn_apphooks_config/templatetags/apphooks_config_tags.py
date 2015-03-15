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
    app_name = ''
    config = None
    namespace = kwargs.pop('namespace', None)

    if not namespace:
        namespace, config = get_app_instance(context['request'])

    if config:
        app_name = config.cmsapp.app_name + ':'
    elif namespace:
        app_name = namespace + ':'

    if kwargs:
        return urlresolvers.reverse(
            '{0:s}{1:s}'.format(app_name, view_name),
            kwargs=kwargs, current_app=namespace)
    elif args:
        return urlresolvers.reverse(
            '{0:s}{1:s}'.format(app_name, view_name),
            args=args, current_app=namespace)
    else:
        return urlresolvers.reverse(
            '{0:s}{1:s}'.format(app_name, view_name),
            current_app=namespace)
