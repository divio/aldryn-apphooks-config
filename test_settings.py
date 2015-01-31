from distutils.version import LooseVersion

HELPER_SETTINGS = dict(
    TIME_ZONE='Europe/Zurich',
    LANGUAGES=(
        ('en', 'English'),
        ('de', 'German'),
    ),
    INSTALLED_APPS=[
        'app_data',
        'djangocms_text_ckeditor',
        'cms.test_utils.project.sampleapp',
        'aldryn_apphooks_config.tests.utils.example',
    ],
    MIGRATION_MODULES={
        'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
    }
)


def run():
    import sys
    import django
    from djangocms_helper import runner
    sys.argv.insert(1, 'aldryn_apphooks_config')
    sys.argv.insert(2, 'test')
    if LooseVersion(django.get_version()) < LooseVersion('1.6'):
        sys.argv.insert(3, '--runner=discover_runner.DiscoverRunner')
    runner.cms('aldryn_apphooks_config')

if __name__ == "__main__":
    run()