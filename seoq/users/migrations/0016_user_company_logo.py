# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-31 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_user_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
