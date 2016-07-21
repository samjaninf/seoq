# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView-
    url(
        regex=r'^seoqtool-example/$',
        view=views.BasicQscraperUseView.as_view(),
        name='tool_example'
    ),
    url(regex=r'(?P<slug>[\w-]+)/www/(?P<netloc>[\w_\-\.]+)/$',
        view=views.SEOQURLFriendlyDetail.as_view(),
        name='seoq_url_friendly_detail'),
    url(
        regex=r'^create-variable/$',
        view=views.CreateVariableView.as_view(),
        name='create_variable'
    ),
    url(
        regex=r'^variables/$',
        view=views.VariableListView.as_view(),
        name='variable_list'
    ),
]
