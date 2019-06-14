# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import common
from simple_history.models import HistoricalRecords

class Material(models.Model):
    history = HistoricalRecords()
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
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)

    def getPricePerUnit(self):
        return float(self.StackBuyPrice) / float(self.StackSize)

    def assetCheck(self):
        if len(self.IconAssetID.replace(" ", "")) == 0 or len(self.TextSpriteAssetID.replace(" ", "")) == 0 or len(self.TextSpriteEntry.replace(" ", "")) == 0:
            return "⚠️ missing asset ID!"
        return "✔️"

    def collect_modules(self, amount=1):
        local_modules = {}
        module_inputs = ModuleInputMaterialAmount.objects.filter(Material=self)
        for module_input in module_inputs:
            # add module
            module = module_input.Module

            # safety check
            if module.id in local_modules:
                local_modules[module.id]["amount"] += module_input.Amount * amount
            else:
                local_modules[module.id] = {
                    "name": module.Name,
                    "amount": module_input.Amount * amount,
                    "cost": module.rawMaterialCost(),
                    "id": module.id,
                    "icon": module.IconAssetID
                }

            # get modules made from this one recursively
            sub_modules = module.Material.collect_modules(module_input.Amount)
            for module_id, sub_module in sub_modules.items():
                
                if module_id in local_modules:
                    local_modules[module_id]["amount"] += sub_module["amount"] * amount
                else:
                    local_modules[module_id] = sub_module
                    local_modules[module_id]["amount"] *= amount

        return local_modules


class ModuleSlotType(models.Model):
    history = HistoricalRecords()
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
    history = HistoricalRecords()
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
    history = HistoricalRecords()
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

class ModuleResearchDataYield(models.Model):
    history = HistoricalRecords()
    Module = models.ForeignKey("Module", related_name="ResearchDataYield")
    ResearchDataType = models.ForeignKey("Research.ResearchDataType", related_name="Modules")
    Amount = models.IntegerField()

    def getJsonObject(self):
        return {
            "DataTypeID": self.ResearchDataType.id,
            "Amount": self.Amount,
        }

    class Meta:
        verbose_name = 'Module Research Data Yield'
        verbose_name_plural = 'Module Research Data Yields'

    def __unicode__(self):
        return u"%s: %d" % (self.ResearchDataType, self.Amount)

class Module(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    FitsIntoSlot = models.ForeignKey(ModuleSlotType, related_name="FittingModule", null=True, blank=True)
    Material = models.ForeignKey(Material)
    OutputAmount = models.IntegerField(default=1)
    BaseMarketPrice = models.FloatField(default=1)
    BaseMarketCapacity = models.IntegerField(default=50)
    MarketRecoveryFactor = models.FloatField(default=0.5)

    def getJsonObject(self):
        fitsIntoSlot = 0
        if self.FitsIntoSlot:
            fitsIntoSlot = self.FitsIntoSlot.id

        features = [feature.getJsonObject() for feature in self.Features.all()]
        featureRequirements = [featureReq.getJsonObject() for featureReq in self.FeatureRequirements.all()]
        inputMaterials = [mat.getJsonObject() for mat in self.InputMaterials.all()]
        researchDataYield = [resYield.getJsonObject() for resYield in self.ResearchDataYield.all()]

        return {
            "Name":self.Name,
            "IconAssetID":self.IconAssetID,
            "MaterialID":self.Material.id,
            "FitsIntoSlot":fitsIntoSlot,
            "Features":features,
            "FeatureRequirements":featureRequirements,
            "InputMaterials":inputMaterials,
            "ResearchDataYield":researchDataYield,
            "OutputAmount":self.OutputAmount,
            "BaseMarketPrice":self.BaseMarketPrice,
            "BaseMarketCapacity":self.BaseMarketCapacity,
            "MarketRecoveryFactor":self.MarketRecoveryFactor
        }

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)

    def slot(self):
        return unicode(self.FitsIntoSlot)

    def rawMaterialCost(self):
        totalCost = 0
        for inputMat in self.InputMaterials.all():
            moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
            if moduleMatQuery.exists():
                totalCost += moduleMatQuery.all()[0].rawMaterialCost() * inputMat.Amount
            else:
                totalCost += inputMat.Material.getPricePerUnit() * inputMat.Amount
        return totalCost / float(self.OutputAmount)

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
                        "amount": inputMat.Amount / float(self.OutputAmount),
                        "totalcost": inputMat.Amount * inputMat.Material.getPricePerUnit() / float(self.OutputAmount),
                        "icon": inputMat.Material.IconAssetID
                    }
        return localMaterials


class ModuleInputMaterialAmount(models.Model):
    history = HistoricalRecords()
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
    history = HistoricalRecords()
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
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True)
    Type = models.IntegerField(choices=common.FeatureTypeChoices, default=common.BINARY)
    ComplementaryFeature = models.ForeignKey("ProductFeature", related_name="MainFeature", null=True, blank=True)
    SymbolAssetID = models.CharField(max_length=255)
    HelperEmoji = models.CharField(max_length=4)

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
        return unicode(self.HelperEmoji + " " +  self.Name)

class ProductFunctionFeatureRequirement(models.Model):
    history = HistoricalRecords()
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
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    IconAssetID = models.CharField(max_length=255)
    ViableProductTypes = models.ManyToManyField(ProductType, related_name="PossibleFunctions")
    BaseMarketPrice = models.IntegerField(default=100)
    BaseMarketCapacity = models.IntegerField(default=50)
    MarketRecoveryFactor = models.FloatField(default=0.5)

    def getJsonObject(self):
        featureRequirements = []
        for req in self.FeatureRequirements.all():
            featureRequirements.append(req.getJsonObject())
        productTypes = []
        for product in self.ViableProductTypes.all():
            productTypes.append(product.id)
        return {
            "Name":self.Name,
            "IconAssetID":self.IconAssetID,
            "ViableProductTypes":productTypes,
            "FeatureRequirements":featureRequirements,
            "BaseMarketPrice":self.BaseMarketPrice,
            "BaseMarketCapacity":self.BaseMarketCapacity,
            "MarketRecoveryFactor":self.MarketRecoveryFactor
        }

    class Meta:
        verbose_name = 'Product Function'
        verbose_name_plural = 'Product Functions'
        ordering = ['id']

    def __unicode__(self):
        return self.Name
