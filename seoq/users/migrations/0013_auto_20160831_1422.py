# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-31 14:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20160825_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='website_url1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='website_url2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='website_url3',
        ),
        migrations.RemoveField(
            model_name='user',
            name='website_url4',
        ),
    ]
