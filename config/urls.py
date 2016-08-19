# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from balystic import views as balystic_views
from seoq.core import views as core_views
from seoq.payments_seoq import views as payments_seoq

from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', core_views.HomeView.as_view(template_name='pages/home.html'),
        name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'),
        name='about'),
    # Needed cause django-braces uses the account prefix for LoginRequiredMixin
    url(r'^accounts/login/$',
        balystic_views.LoginView.as_view(), name='account_login'),
    url(r'^accounts/login/$',
        balystic_views.LoginView.as_view(), name='balystic_login'),
    url(r'^accounts/logout/$',
        balystic_views.LogoutView.as_view(), name='balystic_logout'),
    url(r'^users/edit/(?P<username>[-\w.]+)/$',
        balystic_views.CommunityUserUpdate.as_view(),
        name='balystic_user_update'),
    url(r'^accounts/signup/$',
        balystic_views.UserSignupView.as_view(), name='balystic_signup'),
    url(r'^seo-directory/$', core_views.SEODirectoryUserList.as_view(),
        name='directory'),

    url(r'^seo-directory/(?P<username>[\w.@+-]+)/$',
        core_views.PublicUserDetailView.as_view(),
        name='public_profile'),

    url(r'^website-owners/$',
        TemplateView.as_view(template_name='pages/owners.html'),
        name='owners'),
    # url(r'^join/$', TemplateView.as_view(template_name='pages/join.html'),
    #     name='join'),
    url(r'^seo-professionals/$', TemplateView.as_view
        (template_name='pages/professionals.html'),
        name='professionals'),
    url(r'^seo-students/$', TemplateView.as_view
        (template_name='pages/students.html'),
        name='students'),
    url(r'^order/(?P<pk>\d+)/$',
        payments_seoq.OrderView.as_view(), name='order'),
    url(r'^order/(?P<pk>\d+)/payment/success/$',
        payments_seoq.OrderPaymentReturnView.as_view(status='success'),
        name='order_payment_success'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^', include('seoq.users.urls', namespace='users')),
    url(r'^qa/.*$',
        RedirectView.as_view(
            url='http://seoq.app.balystic.com/questions-and-answers/',
            permanent=False), name='balystic_qa'),
    url(r'^', include('balystic.urls')),
    url(r'^', include('seoq.seoqtool.urls', namespace='seoqtool')),
    url(r'^', include('plans.urls')),

    # Your stuff: custom urls includes go here
    # CompaniesRedirectView
    url(r'^seo-companies/(?P<slug>[-\w.]+)/$',
        core_views.CompaniesRedirectView.as_view(),
        name='seo_companies_redirect'),
    url(r'^(?P<slug>[-\w.]+)/$',
        core_views.ArchivedBlogRedirectView.as_view(), name='archived_blog'),


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
