# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seoqtool', '0002_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='site_score',
            field=models.FloatField(default=0),
        ),
    ]