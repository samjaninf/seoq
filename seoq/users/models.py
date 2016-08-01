# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    fb_account = models.URLField(blank=True, max_length=255)
    twitter_account = models.URLField(blank=True, max_length=255)
    linkedin_account = models.URLField(blank=True, max_length=255)
    title = models.CharField(blank=True, max_length=255)
    about = models.TextField(_("About You"), blank=True, default='')
    profile_picture = models.ImageField(
        null=True,
        upload_to='profile/')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
