# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-28 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developmentproject',
            name='RequiredProjects',
            field=models.ManyToManyField(blank=True, related_name='RequiredForProjects', to='Research.DevelopmentProject'),
        ),
    ]
