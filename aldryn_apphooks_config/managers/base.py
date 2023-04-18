from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.translation import gettext

from ..utils import get_apphook_field_names


class QuerySetMixin:
    def namespace(self, namespace, to=None):
        """
        Filter by namespace. Try to guess which field to use in lookup.
        Accept 'to' argument if you need to specify.
        """
        fields = get_apphook_field_names(self.model)
        if not fields:
            raise ValueError(
                gettext("Can't find any relation to an ApphookConfig model in {0}").format(self.model.__name__)
            )
        if to and to not in fields:
            raise ValueError(
                gettext("Can't find relation to ApphookConfig model named " '"{0}" in "{1}"').format(
                    to, self.model.__name__
                )
            )
        if len(fields) > 1 and to not in fields:
            raise ValueError(
                gettext(
                    '"{0}" has {1} relations to an ApphookConfig model.'
                    ' Please, specify which one to use in argument "to".'
                    " Choices are: {2}"
                ).format(self.model.__name__, len(fields), ", ".join(fields))
            )
        else:
            if not to:
                to = fields[0]

        lookup = "{}__namespace".format(to)
        kwargs = {lookup: namespace}
        return self.filter(**kwargs)


class ManagerMixin:
    def namespace(self, namespace, to=None):
        return self.get_queryset().namespace(namespace, to=to)


class AppHookConfigQuerySet(QuerySetMixin, QuerySet):
    pass


class AppHookConfigManager(ManagerMixin, Manager):
    """
    Manager intended to use in models that has relations to apphooks
    configs. Add the namespace method to manager and queryset that should
    be used to filter objects by it namespace.
    """

    def get_queryset(self):
        return AppHookConfigQuerySet(self.model, using=self.db)
