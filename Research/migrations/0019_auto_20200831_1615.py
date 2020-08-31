# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-08-31 14:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0018_auto_20200831_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprogressnode',
            name='UnlocksPolicies',
            field=models.CharField(blank=True, default='', max_length=500, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='progressnode',
            name='UnlocksPolicies',
            field=models.CharField(blank=True, default='', max_length=500, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
