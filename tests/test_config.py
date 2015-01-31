# -*- coding: utf-8 -*-
from cms import api
from djangocms_helper.base_test import BaseTestCase
from django.conf import settings
from cms.utils import get_cms_setting
from tests.utils.example.models import ExampleConfig


class AppHookConfigTestCase(BaseTestCase):

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page', self.template, self.language, published=True)

        self.ns_app_1 = ExampleConfig.objects.create(namespace='app1')
        self.ns_app_1.app_data.config.property = 'app2_property'
        self.ns_app_2 = ExampleConfig.objects.create(namespace='app2')
        self.ns_app_2.app_data.config.property = 'app2_property'

        self.page_1 = api.create_page(
            'page_1', self.template, self.language, published=True,
            parent=self.root_page,
            apphook='ExampleApp',
            apphook_namespace=self.ns_app_1.namespace)
        self.page_2 = api.create_page(
            'page_2', self.template, self.language, published=True,
            parent=self.root_page,
            apphook='ExampleApp',
            apphook_namespace=self.ns_app_2.namespace)

        for page in self.root_page, self.page_1, self.page_2:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)

    def test_app_1_list(self):
        pass