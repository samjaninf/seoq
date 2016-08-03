# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from balystic import views as balystic_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'),
        name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'),
        name='about'),
    # Needed because django-braces uses the account prefix for LoginRequiredMixin
    url(r'^accounts/login/$', balystic_views.LoginView.as_view(), name='account_login'),
    url(r'^accounts/login/$', balystic_views.LoginView.as_view(), name='balystic_login'),
    url(r'^accounts/logout/$', balystic_views.LogoutView.as_view(), name='balystic_logout'),
    url(r'^seo-directory/$', TemplateView.as_view(template_name='pages/users_directory_page.html'),
        name='directory'),
    url(r'^website-owners/$', TemplateView.as_view(template_name='pages/owners.html'),
        name='owners'),
    # url(r'^join/$', TemplateView.as_view(template_name='pages/join.html'),
    #     name='join'),
    url(r'^seo-professionals/$', TemplateView.as_view
        (template_name='pages/professionals.html'),
        name='professionals'),
    url(r'^seo-students/$', TemplateView.as_view
        (template_name='pages/students.html'),
        name='students'),
    url(r'^seo-score/$', TemplateView.as_view
        (template_name='pages/score.html'),
        name='score'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('seoq.users.urls', namespace='users')),
    url(r'^', include('balystic.urls')),
    url(r'^', include('seoq.seoqtool.urls', namespace='seoqtool')),
    url(r'^api/', include('seoq.api.urls', namespace='api')),
    url(r'^', include('plans.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
