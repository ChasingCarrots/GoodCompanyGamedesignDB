# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-09-25 10:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BalancingHelper', '0013_auto_20190712_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sampleproduct',
            name='ProductFunction',
        ),
        migrations.RemoveField(
            model_name='sampleproduct',
            name='ProductType',
        ),
    ]
