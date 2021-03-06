# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-07-23 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectTypes', '0026_auto_20190712_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildabelCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Icon', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='buildableproperty',
            name='Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ObjectTypes.BuildabelCategory'),
        ),
        migrations.AddField(
            model_name='historicalbuildableproperty',
            name='Category',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ObjectTypes.BuildabelCategory'),
        ),
    ]
