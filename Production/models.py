# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import common
from simple_history.models import HistoricalRecords

class Material(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255, help_text="The asset id of the icon of this material.")
    ModelAssetID = models.CharField(max_length=255, help_text="The asset id of the model for this material.", blank=True)
    TextSpriteAssetID = models.CharField(max_length=255, help_text="The asset id of the TMP spritesheet that contains the text-sprite for this material.", blank=True)
    TextSpriteEntry = models.CharField(max_length=255, help_text="The name of the icon of this material within the TMP spritesheet", blank=True)
    SizeType = models.IntegerField(choices=common.SizeTypeChoices)
    StackSize = models.IntegerField()
    StackBuyPrice = models.IntegerField()

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
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
    Description = models.CharField(max_length=255, blank=True)
    IsOptional = models.BooleanField()

    def getJsonObject(self):
        return {
            "Name":self.Name,
            "Description":self.Description,
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
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    FitsIntoSlot = models.ForeignKey(ModuleSlotType, related_name="FittingModule", null=True, blank=True)
    Material = models.ForeignKey(Material)
    OutputAmount = models.IntegerField(default=1)
    BaseMarketPrice = models.FloatField(default=1)
    BaseMarketCapacity = models.IntegerField(default=50)
    MarketRecoveryFactor = models.FloatField(default=0.5)
    AssemblyTime = models.FloatField(default=5)

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
            "Description": self.Description,
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
            "MarketRecoveryFactor":self.MarketRecoveryFactor,
            "AssemblyTime":self.AssemblyTime
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
                    inputModMaterial["amount"] *= inputMat.Amount / float(self.OutputAmount)
                    inputModMaterial["totalcost"] *= inputMat.Amount / float(self.OutputAmount)
                    if inputModMaterialID in localMaterials:
                        localMaterials[inputModMaterialID]["amount"] += inputModMaterial["amount"]
                        localMaterials[inputModMaterialID]["totalcost"] += inputModMaterial["totalcost"]
                    else:
                        localMaterials[inputModMaterialID] = inputModMaterial
            else:
                inputModMaterialID = inputMat.Material.id
                if inputModMaterialID in localMaterials:
                    localMaterials[inputModMaterialID]["amount"] += inputMat.Amount / float(self.OutputAmount)
                    localMaterials[inputModMaterialID]["totalcost"] += inputMat.Amount * inputMat.Material.getPricePerUnit() / float(self.OutputAmount)
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


class ProductTypeSlotUIPosition(models.Model):
    productType = models.ForeignKey("ProductType", related_name="SlotUIPositions")
    slotType = models.ForeignKey(ModuleSlotType)
    x = models.IntegerField()
    y = models.IntegerField()

    class Meta:
        verbose_name = 'ProductType Slot UI Position'
        verbose_name_plural = 'ProductType Slot UI Positions'

    def __unicode__(self):
        return u"%s %s Slot Position" % (unicode(self.productType), unicode(self.slotType))


class ProductType(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    BigImageAssetID = models.CharField(max_length=255)
    Slots = models.ManyToManyField(ModuleSlotType, related_name="UsedInProductType")
    BaseMarketPrice = models.IntegerField(default=100)
    BaseMarketMaxPriceFactor = models.FloatField(default=5)
    BaseMarketCurvePotential = models.FloatField(default=2)
    RequiredDiscoveryPoints = models.IntegerField(default=10)
    MarketTier = models.IntegerField(default=1)


    def getJsonObject(self):
        slots = []
        for slot in self.Slots.all():
            posX = 0
            posY = 0
            slotUIQuery = ProductTypeSlotUIPosition.objects.filter(productType=self, slotType=slot)
            if slotUIQuery.exists():
                uiPos = slotUIQuery[0]
                posX = uiPos.x
                posY = uiPos.y
            slots.append({
                "SlotID": slot.id,
                "UIPos": {
                    "x": posX,
                    "y": posY
                }
            })
        featureRequirements = []
        for req in self.MandatoryFeatures.all():
            featureRequirements.append(req.getJsonObject())
        optionalFeatures = []
        for optional in self.OptionalFeatures.all():
            optionalFeatures.append(optional.getJsonObject())
        drawbacks = []
        for drawback in self.Drawbacks.all():
            drawbacks.append(drawback.getJsonObject())
        return {
            "Name": self.Name,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "BigImageAssetID": self.BigImageAssetID,
            "SlotTypes": slots,
            "BaseMarketPrice": self.BaseMarketPrice,
            "BaseMarketMaxPriceFactor": self.BaseMarketMaxPriceFactor,
            "BaseMarketCurvePotential": self.BaseMarketCurvePotential,
            "MandatoryFeatures": featureRequirements,
            "OptionalFeatures": optionalFeatures,
            "Drawbacks": drawbacks
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
    ComplementaryFeature = models.ForeignKey("self", related_name="MainFeature", blank=True, null=True)
    SymbolAssetID = models.CharField(max_length=255)
    HelperEmoji = models.CharField(max_length=4)

    def getJsonObject(self):

        complementary = 0
        if self.ComplementaryFeature:
            complementary = self.ComplementaryFeature.id

        mainfeature = 0
        if self.MainFeature.all():
            mainfeature = self.MainFeature.all()[0].id

        return {
            "Name": self.Name,
            "Description": self.Description,
            "Type": self.Type,
            "Complementary": complementary,
            "MainFeature": mainfeature,
            "SymbolAssetID": self.SymbolAssetID,
        }

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'

    def __unicode__(self):
        return unicode(self.HelperEmoji + " " + self.Name)


class ProductTypeFeatureRequirement(models.Model):
    history = HistoricalRecords()
    Function = models.ForeignKey(ProductType, related_name="MandatoryFeatures")
    Feature = models.ForeignKey(ProductFeature, related_name="RequiredInProductTypes")
    MinValue = models.IntegerField(default=1)
    MaxValue = models.IntegerField(default=10)

    def getJsonObject(self):
        return {
            "FeatureID": self.Feature.id,
            "MinValue": self.MinValue,
            "MaxValue": self.MaxValue,
        }

    class Meta:
        verbose_name = 'Mandatory Feature'
        verbose_name_plural = 'Mandatory Features'

    def getRatingValue(self, value):
        if self.MinValue < self.MaxValue and self.Feature.Type == common.ADDITIVE:
            n = float(value - self.MinValue) / float(self.MaxValue - self.MinValue)
            if n > 1:
                n = 1
            elif n < 0:
                n = 0
            return n
        return 0

    def __unicode__(self):
        return u"%d/%d x %s" % (self.MinValue, self.MaxValue, unicode(self.Feature))


class ProductTypeOptionalFeatures(models.Model):
    history = HistoricalRecords()
    Function = models.ForeignKey(ProductType, related_name="OptionalFeatures")
    Feature = models.ForeignKey(ProductFeature, related_name="OptionalInProductTypes")
    MinValue = models.IntegerField(default=0)
    MaxValue = models.IntegerField(default=10)

    def getJsonObject(self):
        return {
            "FeatureID": self.Feature.id,
            "MinValue": self.MinValue,
            "MaxValue": self.MaxValue,
        }

    class Meta:
        verbose_name = 'Optional Feature'
        verbose_name_plural = 'Optional Features'

    def __unicode__(self):
        return u"%d - %d x %s" % (self.MinValue, self.MaxValue, unicode(self.Feature))

    def getRatingValue(self, value):
        if self.MinValue <= self.MaxValue:
            n = float(value - (self.MinValue - 1)) / float(self.MaxValue - (self.MinValue - 1))
            if n > 1:
                n = 1
            elif n < 0:
                n = 0
            return n
        return 0


class ProductTypeDrawbacks(models.Model):
    history = HistoricalRecords()
    ProductType = models.ForeignKey(ProductType, related_name="Drawbacks")
    Feature = models.ForeignKey(ProductFeature, related_name="DrawbackInProductTypes")
    MinValue = models.IntegerField(default=0)
    MaxValue = models.IntegerField(default=10)

    def getJsonObject(self):
        return {
            "FeatureID": self.Feature.id,
            "MinValue": self.MinValue,
            "MaxValue": self.MaxValue,
        }

    class Meta:
        verbose_name = 'Drawback'
        verbose_name_plural = 'Drawbacks'

    def __unicode__(self):
        return u"%d - %d x %s" % (self.MinValue, self.MaxValue, unicode(self.Feature))

    def getRatingValue(self, value):
        if self.MinValue <= self.MaxValue:
            n = float(value - (self.MinValue - 1)) / float(self.MaxValue - (self.MinValue - 1))
            if n > 1:
                n = 1
            elif n < 0:
                n = 0
            return n
        return 0
