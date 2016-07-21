from __future__ import unicode_literals

from django.db import models


# Create your models here.


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
