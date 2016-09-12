# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20160911_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=200)),
                ('permalink', models.CharField(max_length=100, unique=True)),
                ('page_body', models.TextField(verbose_name='body')),
                ('show', models.BooleanField(default=True)),
            ],
        ),
    ]
