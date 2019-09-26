# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-26 15:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0052_auto_20190926_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmodulefeaturerequirement',
            name='Module',
        ),
        migrations.RemoveField(
            model_name='historicalmodulefeaturerequirement',
            name='ProductFeature',
        ),
        migrations.RemoveField(
            model_name='historicalmodulefeaturerequirement',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='modulefeaturerequirement',
            name='Module',
        ),
        migrations.RemoveField(
            model_name='modulefeaturerequirement',
            name='ProductFeature',
        ),
        migrations.DeleteModel(
            name='HistoricalModuleFeatureRequirement',
        ),
        migrations.DeleteModel(
            name='ModuleFeatureRequirement',
        ),
    ]