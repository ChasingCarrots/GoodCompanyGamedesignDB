# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-20 15:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0014_auto_20180917_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildableproperty',
            name='BuildCost',
        ),
    ]
