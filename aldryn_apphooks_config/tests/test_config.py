# -*- coding: utf-8 -*-
from aldryn_apphooks_config.utils import get_app_instance
from aldryn_apphooks_config.managers import AppHookConfigManager

from cms import api
from cms.apphook_pool import apphook_pool
from cms.utils import get_cms_setting
from django.core.urlresolvers import reverse
from django.http import SimpleCookie
from django.utils.encoding import force_text
from django.utils.six import StringIO
from django.conf import settings
from djangocms_helper.base_test import BaseTestCase


from .utils.example.models import (
    AnotherExampleConfig, ExampleConfig, Article, News, TranslatableArticle
)


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
        request = self.request_factory.get('/en/sample/login/')
        request.user = self.user
        request.session = {}
        request.cookies = SimpleCookie()
        request.errors = StringIO()

        # when config is requested on a non-CMS url, just return empty data
        with self.settings(ROOT_URLCONF='cms.test_utils.project.urls'):
            config = get_app_instance(request)
            self.assertEqual((u'', None), config)

    def test_config_str(self):
        app = apphook_pool.get_apphook(self.page_1.application_urls)
        self.assertEqual('%s / %s' % (force_text(app.name), self.ns_app_1.namespace), force_text(self.ns_app_1))

    def test_admin_url(self):
        app = apphook_pool.get_apphook(self.page_1.application_urls)
        url = app.get_config_add_url()
        try:
            self.assertEqual(url, reverse('admin:%s_%s_add' % (ExampleConfig._meta.app_label,
                                                               ExampleConfig._meta.model_name)))
        except AttributeError:  #NOQA
            self.assertEqual(url, reverse('admin:%s_%s_add' % (ExampleConfig._meta.app_label,
                                                               ExampleConfig._meta.module_name)))

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

    def test_apphook_manager_on_simple_model(self):
        ns_app_3 = ExampleConfig.objects.create(namespace='app3')
        ns_app_3.app_data.config.property = 'app3_property'
        ns_app_3.save()

        Article.objects.create(title='article_1_app_1',
                               slug='article_1_app_1',
                               section=self.ns_app_1)
        Article.objects.create(title='article_2_app_1',
                               slug='article_2_app_1',
                               section=self.ns_app_1)
        Article.objects.create(title='article_1_app_2',
                               slug='article_1_app_2',
                               section=self.ns_app_2)

        self.assertEqual(
            2, Article.objects.namespace(self.ns_app_1.namespace).count()
        )
        self.assertEqual(
            1, Article.objects.namespace(self.ns_app_2.namespace).count()
        )
        self.assertEqual(
            0, Article.objects.namespace(ns_app_3.namespace).count()
        )
        self.assertEqual(
            0, Article.objects.namespace('').count()
        )

    def test_apphook_manager_on_model_with_two_configs(self):
        ans_config_1 = AnotherExampleConfig.objects.create(namespace='config1')
        ans_config_2 = AnotherExampleConfig.objects.create(namespace='config2')
        News.objects.create(title='news_1_app_1_config1',
                            slug='news_1_app_1_config1',
                            section=self.ns_app_1,
                            config=ans_config_1)
        News.objects.create(title='news_2_app_1_config2',
                            slug='news_2_app_1_config2',
                            section=self.ns_app_1,
                            config=ans_config_2)
        msg = ("'{0}' has {1} relations to an ApphookConfig model."
               " Please, specify which one to use in argument 'to'."
               " Choices are: {2}".format('News', '2', 'section, config'))
        self.assertRaisesMessage(
            ValueError, msg, News.objects.namespace, ans_config_1.namespace
        )
        self.assertEqual(
            1, News.objects.namespace(ans_config_1.namespace,
                                      to='config').count()
        )
        self.assertEqual(
            2, News.objects.namespace(self.ns_app_1.namespace,
                                      to='section').count()
        )

    def test_translatable_apphook_manager(self):
        t1 = TranslatableArticle.objects.language('en').create(
            title='article_1_app_1_en', slug='article_1_app_1_en',
            section=self.ns_app_1
        )
        self.assertEqual(t1.get_current_language(), 'en')
        t2 = TranslatableArticle.objects.language('de').create(
            title='article_2_app_1_de', slug='article_2_app_1_de',
            section=self.ns_app_1
        )
        self.assertEqual(t2.get_current_language(), 'de')

        self.assertEqual(
            2, TranslatableArticle.objects.namespace(self.ns_app_1.namespace)
                                          .count()
        )
        self.assertEqual(
            1,
            TranslatableArticle.objects.namespace(self.ns_app_1.namespace)
                                       .translated('en')
                                       .count()
        )
        self.assertEqual(
            1,
            TranslatableArticle.objects.namespace(self.ns_app_1.namespace)
                                       .translated('de')
                                       .count()
        )
