# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-29 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20161009_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.BooleanField(default=True),
        ),
    ]
