# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^kw-score/$',
        view=views.KeywordsScoreView.as_view(),
        name='keyword_score'
    ),
    url(
        regex=r'^site-score/$',
        view=views.SiteScoreView.as_view(),
        name='site_score'
    ),
    url(
        regex=r'^start-report/$',
        view=views.SiteFormView.as_view(),
        name='start_report'
    ),
]
