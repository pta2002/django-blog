# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 21:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_auto_20160818_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextra',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userextra',
            name='clef_id',
            field=models.BigIntegerField(blank=True),
        ),
    ]
