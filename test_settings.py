HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
    ),
    'INSTALLED_APPS': [
        'app_data',
        'aldryn_newsblog',
        'aldryn_people',
        'easy_thumbnails',
        'parler',
        'djangocms_text_ckeditor',
        'hvad',
        'filer',
        'cms.test_utils.project.sampleapp'
    ],
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_apphooks_config')

if __name__ == "__main__":
    run()