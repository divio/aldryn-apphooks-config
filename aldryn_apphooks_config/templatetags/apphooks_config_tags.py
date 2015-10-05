# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from django import template
from django.core import urlresolvers
from django.core.urlresolvers import NoReverseMatch

from ..utils import get_app_instance

register = template.Library()


@register.simple_tag(takes_context=True)
def namespace_url(context, view_name, *args, **kwargs):
    """
    Returns an absolute URL matching named view with its parameters and the
    provided application instance namespace.

    If no namespace is passed as a kwarg (or it is "" or None), this templatetag
    will look into the request object for the app_config's namespace. If there
    is still no namespace found, this tag will act like the normal {% url ... %}
    template tag.

    Normally, this tag will return whatever is returned by the ultimate call to
    reverse, which also means it will raise NoReverseMatch if reverse() cannot
    find a match. This behaviour can be override by suppling a 'default' kwarg
    with the value of what should be returned when no match is found.
    """

    namespace = kwargs.pop('namespace', None)

    if not namespace:
        namespace, __ = get_app_instance(context['request'])

    if namespace:
        namespace += ':'

    reverse = partial(
        urlresolvers.reverse, '{0:s}{1:s}'.format(namespace, view_name))

    # We're explicitly NOT happy to just re-raise the exception, as that may
    # adversely affect stack traces.
    if 'default' not in kwargs:
        if kwargs:
            return reverse(kwargs=kwargs)
        elif args:
            return reverse(args=args)
        else:
            return reverse()

    default = kwargs.pop('default', None)
    try:
        if kwargs:
            return reverse(kwargs=kwargs)
        elif args:
            return reverse(args=args)
        else:
            return reverse()
    except NoReverseMatch:
        return default
