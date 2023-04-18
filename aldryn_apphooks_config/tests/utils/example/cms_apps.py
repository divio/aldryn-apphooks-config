from cms.apphook_pool import apphook_pool
from django.urls import path, re_path

from aldryn_apphooks_config.app_base import CMSConfigApp

from .models import ExampleConfig
from .views import ArticleDetail, ArticleList


@apphook_pool.register
class ExampleApp(CMSConfigApp):
    name = "Example"
    app_name = "example"
    app_config = ExampleConfig

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            [
                path("", ArticleList.as_view(), name="example_list"),
                re_path(
                    r"^(?P<slug>[\w_-]+)/$",
                    ArticleDetail.as_view(),
                    name="example_detail",
                ),
            ]
        ]
