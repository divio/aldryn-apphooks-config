from django import forms
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _

from .widgets import AppHookConfigWidget


class AppHookConfigFormField(forms.ModelChoiceField):
    def __init__(self, queryset, empty_label="---------", required=True, widget=AppHookConfigWidget, *args, **kwargs):
        super().__init__(queryset=queryset, empty_label=empty_label, required=required, widget=widget, *args, **kwargs)


class AppHookConfigField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.update({"on_delete": getattr(kwargs, "on_delete", CASCADE)})
        if "help_text" not in kwargs:
            kwargs.update(
                {"help_text": _("When selecting a value, the form is reloaded to " "get the updated default")}
            )
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if "form_class" not in kwargs:
            kwargs.update({"form_class": AppHookConfigFormField})
        return super().formfield(**kwargs)
