# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-09 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0007_auto_20180509_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulefeature',
            name='FeatureValue',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='DefaultValue',
            field=models.FloatField(),
        ),
    ]
