# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-05 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_auto_20160805_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
