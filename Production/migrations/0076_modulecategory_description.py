# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-04 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0075_auto_20200220_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulecategory',
            name='Description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
