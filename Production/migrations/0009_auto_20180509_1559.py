# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-09 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0008_auto_20180509_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeature',
            name='MaxRange',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productfeature',
            name='MinRange',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]