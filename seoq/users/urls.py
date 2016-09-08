# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^users/$',
        view=views.UserListView.as_view(),
        name='list'
    ),

    # url(
    #     regex=r'^user_list/$',
    #     view=views.UserListTempView.as_view(),
    #     name='list'
    # ),

    # url(
    #     regex=r'^user-list-recent/$',
    #     view=views.UserListMostRecentTempView.as_view(),
    #     name='list'
    # ),

    # URL pattern for the UserRedirectView
    url(
        regex=r'^users/~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the UserDetailView
    url(
        regex=r'^users/(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),

    #URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
]
