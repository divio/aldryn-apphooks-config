# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

HELPER_SETTINGS = dict(
    TIME_ZONE='Europe/Zurich',
    LANGUAGES=(
        ('en', 'English'),
        ('de', 'German'),
    ),
    PARLER_LANGUAGES={
        None: (
            {'code': 'en', },
            {'code': 'de', },
        ),
        'default': {
            'fallback': 'en',  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
            # the default; let .active_translations() return fallbacks too.
            'hide_untranslated': False,
        }
    },
    INSTALLED_APPS=[
        'app_data',
        'cms.test_utils.project.sampleapp',
        'aldryn_apphooks_config.tests.utils.example',
        'parler'
    ],
)


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_apphooks_config')


if __name__ == '__main__':
    run()
