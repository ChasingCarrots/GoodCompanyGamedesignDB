# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-23 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0022_productfeature_helperemoji'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeature',
            name='HelperEmoji',
            field=models.CharField(max_length=4),
        ),
    ]