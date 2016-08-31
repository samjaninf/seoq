# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from plans.signals import activate_user_plan
from django.db.models import signals
from django.contrib.postgres.fields import JSONField, ArrayField

@python_2_unicode_compatible
class User(AbstractUser):

    EXPERTISE_CHOICES = (
        ('Technical SEO', 'Technical SEO'),
        ('Writer/Blogger', 'Writer/Blogger'),
        ('Google Analytics', 'Google Analytics'),
        ('Link Builder', 'Link Builder'),
        ('SEO Training', 'SEO Training'),
        ('Social Media', 'Social Media'),
        ('Keyword Analyst', 'Keyword Analyst'),
    )

    LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('French', 'French'),
        ('Spanish', 'Spanish'),
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    phone_number = models.CharField(blank=True, max_length=50)
    fb_account = models.URLField(blank=True, max_length=255)
    twitter_account = models.URLField(blank=True, max_length=255)
    linkedin_account = models.URLField(blank=True, max_length=255)
    google_account = models.URLField(blank=True, max_length=255)
    skype = models.CharField(max_length=50, blank=True, default='')
    title = models.CharField(blank=True, max_length=255)
    about = models.TextField(_("About You"), blank=True, default='')
    location = models.CharField(blank=True, max_length=255)
    profile_picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='profile/')
    generics = JSONField(default=dict)
    website_url = models.URLField(blank=True, max_length=255)
    areas_of_expertise = ArrayField(
        models.CharField(max_length=50, blank=True,
                         choices=EXPERTISE_CHOICES, default=''),
        default=list
        )
    areas_of_expertise_other = models.CharField(max_length=50, blank=True, default='')
    languages = ArrayField(
        models.CharField(max_length=50, blank=True,
                         choices=LANGUAGE_CHOICES, default=''),
        default=list
        )
    languages_other = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


def user_signed_up_(sender, instance, created, **kwargs):
    """
    Whenever a user signs up, they should be added
    to the default plan.
    """
    activate_user_plan.send(sender=sender, user=instance)

signals.post_save.connect(user_signed_up_, sender=User, weak=False,
                          dispatch_uid='models.user_signed_up_')
