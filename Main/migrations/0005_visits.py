# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-09 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_auto_20160805_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usersVisits', models.IntegerField(default=0)),
                ('botsVisits', models.IntegerField(default=0)),
                ('date', models.TextField()),
            ],
        ),
    ]
