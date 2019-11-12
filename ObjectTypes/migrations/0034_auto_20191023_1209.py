# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-23 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0033_auto_20191021_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildabelcategory',
            name='Order',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='buildableproperty',
            name='OrderInCategory',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicalbuildableproperty',
            name='OrderInCategory',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='buildabelcategory',
            name='Icon',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]