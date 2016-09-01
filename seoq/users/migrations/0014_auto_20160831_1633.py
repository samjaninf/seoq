# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-31 16:33
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20160831_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='google_account',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='skype',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='areas_of_expertise',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('Technical SEO', 'Technical SEO'), ('Writer/Blogger', 'Writer/Blogger'), ('Google Analytics', 'Google Analytics'), ('Link Builder', 'Link Builder'), ('SEO Training', 'SEO Training'), ('Social Media', 'Social Media'), ('Keyword Analyst', 'Keyword Analyst')], default='', max_length=50), default=list, size=None),
        ),
    ]