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
    StackBuyPrice = models.IntegerField()

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "IconAssetID": self.IconAssetID,
            "ModelAssetID": self.ModelAssetID,
            "TextSpriteAssetID": self.TextSpriteAssetID,
            "TextSpriteEntry": self.TextSpriteEntry,
            "SizeType": self.SizeType,
            "StackSize": self.StackSize,
            "StackBuyPrice": self.StackBuyPrice,
        }
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'

    def __unicode__(self):
        return unicode(self.Name)

    def getPricePerUnit(self):
        return float(self.StackBuyPrice) / float(self.StackSize)

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
    FeatureValue = models.IntegerField()

    def getJsonObject(self):
        return {
            "FeatureID":self.ProductFeature.id,
            "FeatureValue":self.FeatureValue,
        }

    class Meta:
        verbose_name = 'Module Feature'
        verbose_name_plural = 'Module Feature'

    def __unicode__(self):
        return u"%s %s: %d" % (self.Module, self.ProductFeature, self.FeatureValue)

class ModuleFeatureRequirement(models.Model):
    Module = models.ForeignKey("Module", related_name="FeatureRequirements")
    ProductFeature = models.ForeignKey("ProductFeature")
    FeatureValue = models.IntegerField()

    def getJsonObject(self):
        return {
            "FeatureID":self.ProductFeature.id,
            "FeatureValue":self.FeatureValue,
        }

    class Meta:
        verbose_name = 'Module Feature Requirement'
        verbose_name_plural = 'Module Feature Requirements'

    def __unicode__(self):
        return u"%s %s: %d" % (self.Module, self.ProductFeature, self.FeatureValue)


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
        featureRequirements = [featureReq.getJsonObject() for featureReq in self.FeatureRequirements.all()]
        inputMaterials = [mat.getJsonObject() for mat in self.InputMaterials.all()]
        return {
            "Name":self.Name,
            "IconAssetID":self.IconAssetID,
            "MaterialID":self.Material.id,
            "FitsIntoSlot":fitsIntoSlot,
            "Features":features,
            "FeatureRequirements":featureRequirements,
            "InputMaterials":inputMaterials,
        }
    
    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    def __unicode__(self):
        return u"%s (Slot: %s)" %(unicode(self.Name),unicode(self.FitsIntoSlot))

    def rawMaterialCost(self):
        totalCost = 0
        for inputMat in self.InputMaterials.all():
            moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
            if moduleMatQuery.exists():
                totalCost += moduleMatQuery.all()[0].rawMaterialCost() * inputMat.Amount
            else:
                totalCost += inputMat.Material.getPricePerUnit() * inputMat.Amount
        return totalCost

    def collectMaterials(self):
        # type (Module) -> {}
        localMaterials = {}
        for inputMat in self.InputMaterials.all():
            moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
            if moduleMatQuery.exists():
                inputModMaterials = moduleMatQuery.all()[0].collectMaterials()
                for inputModMaterialID, inputModMaterial in inputModMaterials.items():
                    inputModMaterial["amount"] *= inputMat.Amount
                    inputModMaterial["totalcost"] *= inputMat.Amount
                    if inputModMaterialID in localMaterials:
                        localMaterials[inputModMaterialID]["amount"] += inputModMaterial["amount"]
                        localMaterials[inputModMaterialID]["totalcost"] += inputModMaterial["totalcost"]
                    else:
                        localMaterials[inputModMaterialID] = inputModMaterial
            else:
                inputModMaterialID = inputMat.Material.id
                if inputModMaterialID in localMaterials:
                    localMaterials[inputModMaterialID]["amount"] += inputMat.Amount
                    localMaterials[inputModMaterialID]["totalcost"] += inputMat.Amount * inputMat.Material.getPricePerUnit()
                else:
                    localMaterials[inputModMaterialID] = {
                        "name": inputMat.Material.Name,
                        "amount": inputMat.Amount,
                        "totalcost": inputMat.Amount * inputMat.Material.getPricePerUnit(),
                    }
        return localMaterials


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
    Description = models.TextField(blank=True)
    Type = models.IntegerField(choices=common.FeatureTypeChoices, default=common.MAXIMUM)
    SymbolAssetID = models.CharField(max_length=255)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
            "Type": self.Type,
            "SymbolAssetID": self.SymbolAssetID,
        }

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'

    def __unicode__(self):
        return unicode(self.Name)

class ProductFunctionFeatureRequirement(models.Model):
    Function = models.ForeignKey("ProductFunction", related_name="FeatureRequirements")
    Feature = models.ForeignKey(ProductFeature, related_name="ProductFunctions")
    FeatureValue = models.IntegerField()

    def getJsonObject(self):
        return {
            "FeatureID":self.Feature.id,
            "FeatureValue":self.FeatureValue,
        }

    class Meta:
        verbose_name = 'Feature Requirement'
        verbose_name_plural = 'Feature Requirements'

    def __unicode__(self):
        return u"%d x %s" %(self.FeatureValue, unicode(self.Feature))

class ProductFunction(models.Model):
    Name = models.CharField(max_length=255)

    def getJsonObject(self):
        featureRequirements = []
        for req in self.FeatureRequirements.all():
            featureRequirements.append(req.getJsonObject())
        return {
            "Name":self.Name,
            "FeatureRequirements":featureRequirements,
        }

    class Meta:
        verbose_name = 'Product Function'
        verbose_name_plural = 'Product Functions'

    def __unicode__(self):
        return self.Name