# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import forms


class AppHookConfigWidget(forms.Select):
    template_name = 'admin/apphook_config_widget.html'

    class Media:
        js = ('js/aldryn_apphooks_config/aldryn_apphooks_config.js',)
