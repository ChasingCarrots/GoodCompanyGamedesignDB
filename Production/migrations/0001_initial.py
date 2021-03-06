# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-18 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('IconAssetID', models.CharField(max_length=255)),
                ('SizeType', models.IntegerField()),
                ('StackSize', models.IntegerField()),
                ('BuyPrice', models.IntegerField()),
                ('SellPrice', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('IconAssetID', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleSlotType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('IsOptional', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ModuleStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Steps', to='Production.Module')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleStepInputMaterialAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField()),
                ('Material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.Material')),
                ('ModuleStep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='InputMaterials', to='Production.ModuleStep')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleStepOutputMaterialAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField()),
                ('Material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.Material')),
                ('ModuleStep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OutputMaterials', to='Production.ModuleStep')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('IconAssetID', models.CharField(max_length=255)),
                ('BigImageAssetID', models.CharField(max_length=255)),
                ('Slots', models.ManyToManyField(to='Production.ModuleSlotType')),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='FitsIntoSlot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.ModuleSlotType'),
        ),
    ]
