# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 10:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0014_auto_20180906_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleInputMaterialAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField()),
                ('Material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.Material')),
            ],
            options={
                'verbose_name': 'Input Material',
                'verbose_name_plural': 'Input Materials',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='Material',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Production.Material'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moduleinputmaterialamount',
            name='Module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='InputMaterials', to='Production.Module'),
        ),
    ]
