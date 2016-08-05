# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^www/(?P<netloc>[\w_\-\.]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        view=views.ArchiveReportView.as_view(),
        name='archive_report'
    ),
    url(
        regex=r'^add-url/$',
        view=views.CreateReportURLView.as_view(),
        name='add_url'
    ),
]
