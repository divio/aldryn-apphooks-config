# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import SimpleCookie
from django.utils.six import StringIO
from aldryn_apphooks_config.utils import get_app_instance
from cms.apphook_pool import apphook_pool
from cms import api
from djangocms_helper.base_test import BaseTestCase
from django.conf import settings
from cms.utils import get_cms_setting
from tests.utils.example.models import ExampleConfig, Article


class AppHookConfigTestCase(BaseTestCase):

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page', self.template, self.language, published=True)

        self.ns_app_1 = ExampleConfig.objects.create(namespace='app1')
        self.ns_app_1.app_data.config.property = 'app1_property'
        self.ns_app_1.save()
        self.ns_app_2 = ExampleConfig.objects.create(namespace='app2')
        self.ns_app_2.app_data.config.property = 'app2_property'
        self.ns_app_2.save()

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
        self.page_3 = api.create_page(
            'page_3', self.template, self.language, published=True,
            parent=self.root_page,
            apphook='SampleApp')

        for page in self.root_page, self.page_1, self.page_2:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)

    def test_configs(self):
        app = apphook_pool.get_apphook(self.page_1.application_urls)
        self.assertEqual(app.get_configs().count(), 2)

    def test_wrong_ns(self):
        app = apphook_pool.get_apphook(self.page_1.application_urls)
        self.assertIsNone(app.get_config('no_app'))

    def test_bad_property(self):
        with self.assertRaises(AttributeError):
            self.ns_app_1.no_property

    def test_app_no_ns(self):
        request = self.get_page_request(self.page_3, self.user)
        config = get_app_instance(request)
        # when config is requested on a non-config apphook, just return empty data
        self.assertEqual((u'', None), config)

    def test_no_page(self):
        request = self.request_factory.get('/en/')
        request.user = self.user
        request.session = {}
        request.cookies = SimpleCookie()
        request.errors = StringIO()

        # when config is requested on a non-CMS url, just return empty data
        with self.settings(ROOT_URLCONF='cms.test_utils.project.sampleapp.urls2'):
            config = get_app_instance(request)
            self.assertEqual((u'', None), config)

    def test_config_str(self):
        app = apphook_pool.get_apphook(self.page_1.application_urls)
        st1 = unicode(self.ns_app_1)
        self.assertEqual('%s / %s' % (unicode(app.name), self.ns_app_1.namespace), st1)

    def test_admin_url(self):
        app = apphook_pool.get_apphook(self.page_1.application_urls)
        url = app.get_config_add_url()
        self.assertEqual(url, reverse('admin:%s_%s_add' % (ExampleConfig._meta.app_label,
                                                           ExampleConfig._meta.model_name)))

    def test_app_1_list_empty(self):
        response = self.client.get('/en/page_1/')
        self.assertContains(response, 'namespace:app1')
        self.assertContains(response, 'property:app1_property')
        self.assertContains(response, 'objects:0')

    def test_app_2_list_empty(self):
        response = self.client.get('/en/page_2/')
        self.assertContains(response, 'namespace:app2')
        self.assertContains(response, 'property:app2_property')
        self.assertContains(response, 'objects:0')

    def test_app_1_list_items(self):
        Article.objects.create(title='article_app_1',
                               slug='article_app_1', section=self.ns_app_1)
        response = self.client.get('/en/page_1/')
        self.assertContains(response, 'namespace:app1')
        self.assertContains(response, 'property:app1_property')
        self.assertContains(response, 'objects:1')

    def test_app_2_list_items(self):
        Article.objects.create(title='article_app_2',
                               slug='article_app_2', section=self.ns_app_2)
        response = self.client.get('/en/page_2/')
        self.assertContains(response, 'namespace:app2')
        self.assertContains(response, 'property:app2_property')
        self.assertContains(response, 'objects:1')