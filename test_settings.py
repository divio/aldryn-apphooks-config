HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
    ),
    'INSTALLED_APPS': [
        'app_data',
        'djangocms_text_ckeditor',
        'cms.test_utils.project.sampleapp',
        'tests.utils.example',
    ],
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_apphooks_config')

if __name__ == "__main__":
    run()