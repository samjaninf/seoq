# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from balystic.client import Client
from .models import User
from .forms import EditProfileForm
from plans.models import UserPlan

from django.conf import settings


class UserDetailView(View):
    template_name = 'users/user_detail.html'

    def get(self, request, username):
        if not request.user.is_authenticated() or\
           request.user.username != str(username):
            return redirect('public_profile', username=username)
        plan = None
        if self.request.user.is_authenticated():
            plan = UserPlan.objects.get(
                user=self.request.user)
        user = Client().get_user_detail(username)
        owner = Client().get_users({'userType': 'owner'})['owner']
        return render(
            request,
            self.template_name,
            {'user': user, 'userplan': plan, 'owner': owner})


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = EditProfileForm

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
