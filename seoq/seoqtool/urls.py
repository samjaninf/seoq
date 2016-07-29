# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^www/(?P<netloc>[\w_\-\.]+)/$',
        view=views.ReportView.as_view(),
        name='report'
    ),
    url(
        regex=r'^www/(?P<netloc>[\w_\-\.]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        view=views.ArchiveReportView.as_view(),
        name='archive_report'
    ),
    url(
        regex=r'^start-report/$',
        view=views.SiteFormView.as_view(),
        name='start_report'
    ),
    url(
        regex=r'^add-url/$',
        view=views.CreateReportURLView.as_view(),
        name='add_url'
    ),

    # url(
    #     regex=r'^seoqtool-example/$',
    #     view=views.BasicQscraperUseView.as_view(),
    #     name='tool_example'
    # ),
    # url(regex=r'(?P<slug>[\w-]+)/www/(?P<netloc>[\w_\-\.]+)/$',
    #     view=views.SEOQURLFriendlyDetail.as_view(),
    #     name='seoq_url_friendly_detail'),
    # url(
    #     regex=r'^create-variable/$',
    #     view=views.CreateVariableView.as_view(),
    #     name='create_variable'
    # ),
    # url(
    #     regex=r'^variables/$',
    #     view=views.VariableListView.as_view(),
    #     name='variable_list'
    # ),
]
