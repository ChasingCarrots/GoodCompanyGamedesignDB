# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-15 14:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0063_auto_20191009_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Module Category',
                'verbose_name_plural': 'Module Categories',
            },
        ),
        migrations.AddField(
            model_name='historicalmodule',
            name='OrderInCategory',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='module',
            name='OrderInCategory',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='historicalmodule',
            name='Category',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Production.ModuleCategory'),
        ),
        migrations.AddField(
            model_name='module',
            name='Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Modules', to='Production.ModuleCategory'),
        ),
    ]
