# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.utils.compat import DJANGO_1_10
from django import forms
from django.utils.html import mark_safe


class AppHookConfigWidget(forms.Select):
    template_name = 'aldryn_apphooks_config/admin/apphook_config_widget.html'

    class Media:
        js = ('js/aldryn_apphooks_config/aldryn_apphooks_config.js',)

    def render(self, name, value, attrs=None, choices=()):
        if choices:  # pragma: no cover
            out = super(AppHookConfigWidget, self).render(name, value, attrs, choices)
        else:
            out = super(AppHookConfigWidget, self).render(name, value, attrs)
        if not DJANGO_1_10:
            return out
        else:
            final_attrs = self.build_attrs(attrs, name=name)
            script = """
            <script>
            (function($) {
                $(document).ready(function () {
                    var sel = $('#%(id)s');
                    if (!sel.val()) {
                        sel.change(function () {
                            $(this).apphook_reload_admin(
                                '%(name)s', $("option:selected",$(this)).val()
                            );
                        });
                    }
                });
            })(django.jQuery);
            </script>
    """ % final_attrs
            return mark_safe(script + out)
