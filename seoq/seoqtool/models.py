from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.db import models


# Create your models here.

REPORT_FREQUENCY = (
    ('daily', 'daily'),
    ('weekly', 'weekly'),
    ('monthly', 'monthly'),
)


class ReportURL(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    frequency = models.CharField(choices=REPORT_FREQUENCY, max_length=7)
    url = models.URLField()
    keywords = models.CharField(max_length=250, blank=True)
    last_analyzed = models.DateTimeField()


class AlgorithmVariable(models.Model):
    name = models.CharField(max_length=250)
    weight = models.FloatField()
    active = models.BooleanField(
        help_text='make sure only one variable per name is active')

    class Meta:
        verbose_name = "Algorithm variable"
        verbose_name_plural = "algorithm variables"

    def __str__(self):
        return self.name + ' = ' + str(self.weight)

    # avoid having more than one active variable with
    # the same name

    def save(self, *args, **kwargs):
        if self.active:
            if self.pk is None:
                AlgorithmVariable.objects.filter(
                    name=self.name).update(active=False)
            else:
                AlgorithmVariable.objects.filter(
                    name=self.name).exclude(
                    pk=self.pk).update(active=False)

        super(AlgorithmVariable, self).save(*args, **kwargs)
