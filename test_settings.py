from distutils.version import LooseVersion

HELPER_SETTINGS = dict(
    TIME_ZONE='Europe/Zurich',
    LANGUAGES=(
        ('en', 'English'),
        ('de', 'German'),
    ),
    PARLER_LANGUAGES={
        None: (
            {'code': 'en',},
            {'code': 'de',},
        ),
        'default': {
            'fallback': 'en',  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
            'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
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

if __name__ == "__main__":
    run()
