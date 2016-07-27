from __future__ import unicode_literals
from django.conf import settings
from django.db import models


# Create your models here.

class Report(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    netloc = models.URLField()
    site_score = models.FloatField(default=0)
    keyword_score = models.FloatField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)


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
