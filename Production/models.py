# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import common

class Material(models.Model):
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255, help_text="The asset id of the icon of this material.")
    ModelAssetID = models.CharField(max_length=255, help_text="The asset id of the model for this material.", blank=True)
    TextSpriteAssetID = models.CharField(max_length=255, help_text="The asset id of the TMP spritesheet that contains the text-sprite for this material.", blank=True)
    TextSpriteEntry = models.CharField(max_length=31, help_text="The name of the icon of this material within the TMP spritesheet", blank=True)
    SizeType = models.IntegerField(choices=common.SizeTypeChoices)
    StackSize = models.IntegerField()
    BuyPrice = models.IntegerField()
    SellPrice = models.IntegerField()

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "IconAssetID": self.IconAssetID,
            "ModelAssetID": self.ModelAssetID,
            "TextSpriteAssetID": self.TextSpriteAssetID,
            "TextSpriteEntry": self.TextSpriteEntry,
            "SizeType": self.SizeType,
            "StackSize": self.StackSize,
            "BuyPrice": self.BuyPrice,
            "SellPrice": self.SellPrice
        }
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'

    def __unicode__(self):
        return unicode(self.Name)

class ModuleSlotType(models.Model):
    Name = models.CharField(max_length=255)
    IsOptional = models.BooleanField()

    def getJsonObject(self):
        return {
            "Name":self.Name,
            "IsOptional":self.IsOptional,
        }
    
    class Meta:
        verbose_name = 'Module Slot Type'
        verbose_name_plural = 'Module Slot Types'

    def __unicode__(self):
        if self.IsOptional:
            return u"%s (optional)" % unicode(self.Name)
        else:
            return unicode(self.Name)

class ModuleFeature(models.Model):
    Module = models.ForeignKey("Module", related_name="Features")
    ProductFeature = models.ForeignKey("ProductFeature")
    FeatureValue = models.FloatField()

    def getJsonObject(self):
        return {
            "FeatureID":self.ProductFeature.id,
            "FeatureValue":self.FeatureValue,
        }

    class Meta:
        verbose_name = 'Module Feature'
        verbose_name_plural = 'Module Feature'

    def __unicode__(self):
        return u"%s %s: %d %s" % (self.Module, self.ProductFeature, self.FeatureValue, self.ProductFeature.Unit)

class Module(models.Model):
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    FitsIntoSlot = models.ForeignKey(ModuleSlotType, related_name="FittingModule", null=True, blank=True)
    Material = models.ForeignKey(Material)

    def getJsonObject(self):
        fitsIntoSlot = 0
        if self.FitsIntoSlot:
            fitsIntoSlot = self.FitsIntoSlot.id

        features = [feature.getJsonObject() for feature in self.Features.all()]
        inputMaterials = [mat.getJsonObject() for mat in self.InputMaterials.all()]
        return {
            "Name":self.Name,
            "IconAssetID":self.IconAssetID,
            "FitsIntoSlot":fitsIntoSlot,
            "Features":features,
            "InputMaterials":inputMaterials,
        }
    
    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    def __unicode__(self):
        return u"%s (Slot: %s)" %(unicode(self.Name),unicode(self.FitsIntoSlot))

class ModuleInputMaterialAmount(models.Model):
    Material = models.ForeignKey(Material)
    Amount = models.IntegerField()
    Module = models.ForeignKey(Module, related_name="InputMaterials")

    def getJsonObject(self):
        return {
            "MaterialID":self.Material.id,
            "Amount":self.Amount,
        }
    
    class Meta:
        verbose_name = 'Input Material'
        verbose_name_plural = 'Input Materials'

    def __unicode__(self):
        return u"%d x %s" %(self.Amount, unicode(self.Material))

class ProductType(models.Model):
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    BigImageAssetID = models.CharField(max_length=255)
    Slots = models.ManyToManyField(ModuleSlotType, related_name="UsedInProductType")

    def getJsonObject(self):
        slots = []
        for slot in self.Slots.all():
            slots.append(slot.id)
        return {
            "Name":self.Name,
            "IconAssetID":self.IconAssetID,
            "BigImageAssetID":self.BigImageAssetID,
            "SlotTypes":slots,
        }
    
    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

    def __unicode__(self):
        return unicode(self.Name)

class ProductFeature(models.Model):
    Name = models.CharField(max_length=255)
    Unit = models.CharField(max_length=8)
    Description = models.TextField()
    PropagationType = models.IntegerField(choices=common.PropagationTypeChoices)
    DefaultValue = models.FloatField()
    MinRange = models.FloatField()
    MaxRange = models.FloatField()

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Unit": self.Unit,
            "Description": self.Description,
            "PropagationType": self.PropagationType,
            "DefaultValue": self.DefaultValue,
            "MinRange": self.MinRange,
            "MaxRange": self.MaxRange
        }

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'

    def __unicode__(self):
        return unicode(self.Name)


