# -*- coding: utf-8 -*-
from django.db.models import ForeignKey, Manager, QuerySet
from parler.managers import TranslatableManager, TranslatableQuerySet



def get_apphook_field_names(model):
    """
    Return all foreign key field names for a AppHookConfig based model
    """
    from .models import AppHookConfig  # avoid circular dependencies
    fields = []
    for field in model._meta.fields:
        if (isinstance(field, ForeignKey)
                and issubclass(field.rel.to, AppHookConfig)):
            fields.append(field)
    return [field.name for field in fields]


class ApphooksConfigQueryset(QuerySet):

    def namespace(self, namespace, to=None):
        """
        Filter by namespace. Try to guess which field to use in lookup.
        Accept 'to' argument if you need to specify.
        """
        fields = get_apphook_field_names(self.model)
        if not fields:
            raise ValueError(
                "Can't find any relation to an ApphookConfig model "
                "in {}".format(self.model.__name__)
            )
        if to and to not in fields:
            raise ValueError(
                "Can't find relation to ApphookConfig model named "
                "'{}' in '{}'".format(to, self.model.__name__)
            )
        if len(fields) > 1 and to not in fields:
            raise ValueError(
                "'{}' has {} relations to an ApphookConfig model."
                " Please, specify which one to use in argument 'to'."
                " Choices are: {}".format(
                    self.model.__name__, len(fields), ", ".join(fields)
                )
            )
        else:
            if not to:
                to = fields[0]

        lookup = '{}__namespace'.format(to)
        kwargs = {lookup: namespace}
        return self.filter(**kwargs)

class ApphooksConfigTranslatableQueryset(ApphooksConfigQueryset,
                                         TranslatableQuerySet):
    pass


class ApphooksConfigManager(Manager):
    """
    Manager intended to use in models that has relations to apphooks
    configs. Add the namespace method to manager and queryset that should
    be used to filter objects by it namespace.
    """
    def get_queryset(self):
        return ApphooksConfigQueryset(self.model, using=self.db)

    def namespace(self, namespace, to=None):
        return self.get_queryset().namespace(namespace, to=to)


class ApphooksConfigTranslatableManager(ApphooksConfigManager,
                                        TranslatableManager):
    """
    Manager intended to use in TranslatableModels that has relations
    to apphooks configs. Add the namespace method to manager and queryset
    that should be used to filter objects by it namespace.
    """
    def get_queryset(self):
        return ApphooksConfigTranslatableQueryset(self.model, using=self.db)
