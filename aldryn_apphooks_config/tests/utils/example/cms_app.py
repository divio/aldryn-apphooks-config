from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .models import ExampleConfig
from .views import ArticleList, ArticleDetail


class ExampleApp(CMSConfigApp):
    name = _('Example')
    urls = [
        patterns('',  # NOQA
            url(r'^$', ArticleList.as_view(), name='example_list'),
            url(r'^(?P<slug>[\w_-]+)/$', ArticleDetail.as_view(), name='example_detail'),
        )
    ]
    app_name = 'example'
    app_config = ExampleConfig


apphook_pool.register(ExampleApp)
