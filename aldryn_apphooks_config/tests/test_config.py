# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path
from copy import deepcopy

from cms import api
from cms.apphook_pool import apphook_pool
from cms.utils import get_cms_setting
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import SimpleCookie
from django.template import RequestContext, Template
from django.utils.encoding import force_text
from django.utils.six import StringIO
from djangocms_helper.base_test import BaseTestCase

from ..utils import get_app_instance, get_apphook_configs, get_apphook_field_names
from .utils.example.models import (
    AnotherExampleConfig, Article, ExampleConfig, News, NotApphookedModel, TranslatableArticle,
)


class AppHookConfigTestCase(BaseTestCase):

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page', self.template, self.language, published=True)

        self.ns_app_1 = ExampleConfig.objects.create(namespace='app1')
        self.ns_app_1.app_data.config.property = 'app1_property'
        self.ns_app_1.app_data.config.published_default = False
        self.ns_app_1.save()
        self.ns_app_2 = ExampleConfig.objects.create(namespace='app2')
        self.ns_app_2.app_data.config.property = 'app2_property'
        self.ns_app_2.app_data.config.published_default = True
        self.ns_app_2.save()
        self.ns_app_3 = AnotherExampleConfig.objects.create(namespace='app3')
        self.ns_app_3.app_data.config.property = 'app3_property'
        self.ns_app_3.app_data.config.published_default = True
        self.ns_app_3.save()

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
        msg = ('"{0}" has {1} relations to an ApphookConfig model.'
               ' Please, specify which one to use in argument "to".'
               ' Choices are: {2}'.format('News', '2', 'section, config'))
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

    def test_get_config_data(self):
        from django.contrib import admin

        article = Article.objects.create(title='news_1_app_1_config1',
                                         slug='news_1_app_1_config1',
                                         section=self.ns_app_1)

        admin.autodiscover()

        admin_instance = admin.site._registry[Article]

        # correct parameter passed by the request
        request = self.get_page_request(self.page_3, self.user)
        request.GET = deepcopy(request.GET)
        request.GET['section'] = self.ns_app_1.pk
        retrieved = admin_instance.get_config_data(request, article, 'property')
        self.assertEqual(retrieved, self.ns_app_1.property)

        # correct parameter passed by the request - no existing object
        request = self.get_page_request(self.page_3, self.user)
        request.GET = deepcopy(request.GET)
        request.GET['section'] = self.ns_app_1.pk
        retrieved = admin_instance.get_config_data(request, Article(), 'property')
        self.assertEqual(retrieved, self.ns_app_1.property)

        # no parameter from request - config retrieved form existing instance
        request = self.get_page_request(self.page_3, self.user)
        retrieved = admin_instance.get_config_data(request, article, 'property')
        self.assertEqual(retrieved, self.ns_app_1.property)

    def test_config_select(self):
        from django.contrib import admin

        article = Article.objects.create(title='news_1_app_1_config1',
                                         slug='news_1_app_1_config1',
                                         section=self.ns_app_1)

        admin.autodiscover()

        admin_instance = admin.site._registry[Article]

        # no object is set, no parameter passed through the request, two namespaces
        request = self.get_page_request(self.page_3, self.user)
        value = admin_instance._app_config_select(request, None)
        self.assertEqual(value, None)

        # object is set, no parameter passed through the request, two namespaces
        request = self.get_page_request(self.page_3, self.user)
        value = admin_instance._app_config_select(request, article)
        self.assertEqual(value, article.section)

        self.ns_app_2.delete()

        # no object is set, no parameter passed through the request, one namespace
        request = self.get_page_request(self.page_3, self.user)
        value = admin_instance._app_config_select(request, None)
        self.assertEqual(value, self.ns_app_1)

    def test_get_config_form(self):
        from django.contrib import admin

        article = Article.objects.create(title='news_1_app_1_config1',
                                         slug='news_1_app_1_config1',
                                         section=self.ns_app_1)

        admin.autodiscover()

        admin_instance = admin.site._registry[Article]

        # no object is set, no parameter passed through the request, two namespaces
        request = self.get_page_request(self.page_3, self.user)
        form = admin_instance.get_form(request, None)
        self.assertEqual(list(form.base_fields.keys()), ['section'])
        self.assertEqual(form.base_fields['section'].initial, None)

        # object is set, normal form is used
        request = self.get_page_request(self.page_3, self.user)
        request.GET = deepcopy(request.GET)
        request.GET['section'] = self.ns_app_1.pk
        form = admin_instance.get_form(request, article)
        self.assertEqual(list(form.base_fields.keys()), ['title', 'slug', 'section', 'published'])
        self.assertEqual(form.base_fields['section'].initial, self.ns_app_1)

        # no object is set, parameter passed through the request
        request = self.get_page_request(self.page_3, self.user)
        request.GET = deepcopy(request.GET)
        request.GET['section'] = self.ns_app_1.pk
        form = admin_instance.get_form(request, None)
        self.assertEqual(list(form.base_fields.keys()), ['title', 'slug', 'section', 'published'])
        self.assertEqual(form.base_fields['section'].initial, self.ns_app_1)

        self.ns_app_2.delete()
        request = self.get_page_request(self.page_3, self.user)
        app_config_default = admin_instance._app_config_select(request, None)
        self.assertEqual(app_config_default, self.ns_app_1)

        # no object is set, no parameter passed through the request, one namespace
        request = self.get_page_request(self.page_3, self.user)
        form = admin_instance.get_form(request, None)
        self.assertEqual(list(form.base_fields.keys()), ['title', 'slug', 'section', 'published'])
        self.assertEqual(form.base_fields['section'].initial, self.ns_app_1)

    def test_admin(self):
        from django.contrib import admin
        admin.autodiscover()

        admin_instance = admin.site._registry[Article]

        # testing behavior when more than 1 namespace instance exists - the selection form
        # should be shown
        request = self.get_page_request(self.page_3, self.user)
        response = admin_instance.add_view(request)
        self.assertContains(response, '$(this).apphook_reload_admin')
        self.assertContains(response, 'aldryn_apphooks_config')
        self.assertContains(response, '<option value="1">%s</option>' % self.ns_app_1)
        self.assertContains(response, '<option value="2">%s</option>' % self.ns_app_2)
        self.assertContains(response, '<h2>Select app config</h2>')

        # only one namespace instance exists, the normal changeform is used
        self.ns_app_2.delete()
        response = admin_instance.add_view(request)
        self.assertContains(response, '$(this).apphook_reload_admin')
        self.assertContains(response, 'aldryn_apphooks_config')
        self.assertContains(response, '<option value="1" selected="selected">%s</option>' % self.ns_app_1)
        self.assertContains(response, '<input id="id_published"')

        self.ns_app_1.app_data.config.published_default = True
        self.ns_app_1.save()
        response = admin_instance.add_view(request)
        self.assertContains(response, '<input checked="checked" id="id_published"')

    def test_templatetag(self):
        article = Article.objects.create(title='news_1_app_1_config1',
                                         slug='news_1_app_1_config1',
                                         section=self.ns_app_1)

        request = self.get_page_request(self.page_1, self.user)
        context = RequestContext(request, {'object': article, 'current_app': self.ns_app_1.namespace})

        template = Template('{% load apphooks_config_tags %}{% namespace_url "example_detail" object.slug %}')
        response = template.render(context)
        self.assertEqual(response, os.path.join(self.page_1.get_absolute_url(), article.slug, ''))

        template = Template('{% load apphooks_config_tags %}{% namespace_url "example_detail" slug=object.slug %}')
        response = template.render(context)
        self.assertEqual(response, os.path.join(self.page_1.get_absolute_url(), article.slug, ''))

        template = Template('{% load apphooks_config_tags %}{% namespace_url "example_list" %}')
        response = template.render(context)
        self.assertEqual(response, self.page_1.get_absolute_url())

        request = self.get_page_request(self.page_2, self.user)
        context = RequestContext(request, {'object': article, 'current_app': self.ns_app_2.namespace})
        template = Template('{% load apphooks_config_tags %}{% namespace_url "example_list" %}')
        response = template.render(context)
        self.assertEqual(response, self.page_2.get_absolute_url())

    def test_apphook_field_name_discovery(self):
        field_names = get_apphook_field_names(Article)
        self.assertEqual(field_names, ['section'])

        field_names = get_apphook_field_names(TranslatableArticle)
        self.assertEqual(field_names, ['section'])

        field_names = get_apphook_field_names(News)
        self.assertEqual(set(field_names), set(['config', 'section']))

        field_names = get_apphook_field_names(NotApphookedModel)
        self.assertEqual(field_names, [])

    def test_apphook_field_name_discovery_from_objects(self):
        field_names = get_apphook_field_names(Article())
        self.assertEqual(field_names, ['section'])

        field_names = get_apphook_field_names(TranslatableArticle())
        self.assertEqual(field_names, ['section'])

        field_names = get_apphook_field_names(News())
        self.assertEqual(set(field_names), set(['config', 'section']))

        field_names = get_apphook_field_names(NotApphookedModel())
        self.assertEqual(field_names, [])

    def test_apphook_config_objects_discovery(self):
        obj = Article(section=self.ns_app_1)
        configs = get_apphook_configs(obj)
        self.assertEqual(configs, [self.ns_app_1])

        obj = TranslatableArticle(section=self.ns_app_1)
        configs = get_apphook_configs(obj)
        self.assertEqual(configs, [self.ns_app_1])

        obj = News(section=self.ns_app_1, config=self.ns_app_3)
        configs = get_apphook_configs(obj)
        self.assertEqual(set(configs), set([self.ns_app_1, self.ns_app_3]))

        obj = NotApphookedModel()
        configs = get_apphook_configs(obj)
        self.assertEqual(configs, [])
