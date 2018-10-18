# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-28 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0018_auto_20180928_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Product Function',
                'verbose_name_plural': 'Product Functions',
            },
        ),
        migrations.CreateModel(
            name='ProductFunctionFeatureRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FeatureValue', models.IntegerField()),
                ('Feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductFunctions', to='Production.ProductFeature')),
                ('Function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FeatureRequirements', to='Production.ProductFunction')),
            ],
            options={
                'verbose_name': 'Feature Requirement',
                'verbose_name_plural': 'Feature Requirements',
            },
        ),
    ]