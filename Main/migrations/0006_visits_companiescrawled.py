# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-09 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_visits'),
    ]

    operations = [
        migrations.AddField(
            model_name='visits',
            name='companiesCrawled',
            field=models.IntegerField(default=0),
        ),
    ]