# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-11-21 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0013_auto_20191023_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='developmentproject',
            name='Tier',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicaldevelopmentproject',
            name='Tier',
            field=models.IntegerField(default=1),
        ),
    ]