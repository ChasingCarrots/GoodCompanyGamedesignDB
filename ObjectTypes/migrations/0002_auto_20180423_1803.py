# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-23 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectLookProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ModelAssetID', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Object Look Property',
                'verbose_name_plural': 'Object Look Properties',
            },
        ),
        migrations.AlterModelOptions(
            name='movableproperty',
            options={'verbose_name': 'Movable Property', 'verbose_name_plural': 'Movable Properties'},
        ),
        migrations.AlterModelOptions(
            name='objecttype',
            options={'verbose_name': 'Object Type', 'verbose_name_plural': 'Object Types'},
        ),
        migrations.AddField(
            model_name='objectlookproperty',
            name='ObjectType',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ObjectLookProperty', to='ObjectTypes.ObjectType'),
        ),
    ]
