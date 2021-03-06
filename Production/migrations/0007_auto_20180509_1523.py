# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-09 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0006_auto_20180507_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FeatureValue', models.IntegerField()),
                ('Module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Features', to='Production.Module')),
            ],
            options={
                'verbose_name': 'Module Feature',
                'verbose_name_plural': 'Module Feature',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Unit', models.CharField(max_length=8)),
                ('Description', models.TextField()),
                ('PropagationType', models.IntegerField(choices=[(0, 'Multiplicative'), (1, 'Minimum'), (2, 'Maximum'), (3, 'Additive'), (4, 'Boolean OR'), (5, 'Boolean AND')])),
                ('DefaultValue', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Product Feature',
                'verbose_name_plural': 'Product Features',
            },
        ),
        migrations.AddField(
            model_name='modulefeature',
            name='ProductFeature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.ProductFeature'),
        ),
    ]
