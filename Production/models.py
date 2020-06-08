# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import common
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from Research.models import *
from BalancingHelper.models import *

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


class ModuleFeature(models.Model):
    history = HistoricalRecords()
    Module = models.ForeignKey("Module", related_name="Features")
    ProductFeature = models.ForeignKey("ProductFeature")
    FeatureValue = models.IntegerField()

    def getJsonObject(self):
        return {
            "FeatureID":self.ProductFeature.id,
            "Value":self.FeatureValue,
        }

    class Meta:
        verbose_name = 'Module Feature'
        verbose_name_plural = 'Module Feature'

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


class ModuleField(models.Model):
    module = models.ForeignKey("Module", related_name="GridFields")
    x = models.IntegerField()
    y = models.IntegerField()

    def getJsonObject(self):
        return {"X": self.x, "Y":self.y}

    class Meta:
        verbose_name = 'Module Field'
        verbose_name_plural = 'Module Fields'

    def __unicode__(self):
        return u"%s GridFields" % (unicode(self.module))

class ModuleCategory(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    Order = models.IntegerField(default=1)
    IconAssetID = models.CharField(max_length=255, null=True, blank=True)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "Order": self.Order
        }

    class Meta:
        verbose_name = "Module Category"
        verbose_name_plural = "Module Categories"

    def __unicode__(self):
        return self.Name


class Module(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    Material = models.ForeignKey(Material)
    OutputAmount = models.IntegerField(default=1)
    BaseMarketPrice = models.FloatField(default=0)
    BaseMarketCapacity = models.IntegerField(default=20)
    AssemblyTime = models.FloatField(default=2)
    SamplingTime = models.FloatField(default=1)
    Category = models.ForeignKey(ModuleCategory, related_name="Modules", null=True, blank=True)
    OrderInCategory = models.IntegerField(default=1)
    Tags = models.CharField(max_length=512, default="", help_text="Separate multiple tags by comma")

    def getJsonObject(self):
        features = [feature.getJsonObject() for feature in self.Features.all()]
        inputMaterials = [mat.getJsonObject() for mat in self.InputMaterials.all()]
        researchDataYield = [resYield.getJsonObject() for resYield in self.ResearchDataYield.all()]
        gridDimensions = [gridDim.getJsonObject() for gridDim in self.GridFields.all()]
        category = 0
        if self.Category:
            category = self.Category.id

        return {
            "Name":self.Name,
            "Description": self.Description,
            "IconAssetID":self.IconAssetID,
            "MaterialID":self.Material.id,
            "Features":features,
            "InputMaterials":inputMaterials,
            "ResearchDataYield":researchDataYield,
            "OutputAmount":self.OutputAmount,
            "BaseMarketPrice":self.BaseMarketPrice,
            "BaseMarketCapacity":self.BaseMarketCapacity,
            "AssemblyTime":self.AssemblyTime,
            "SamplingTime":self.SamplingTime,
            "GridDimensions": gridDimensions,
            "CategoryID": category,
            "OrderInCategory": self.OrderInCategory,
            "Tags": self.Tags
        }

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ['id']

    def __unicode__(self):
        return unicode(self.Name)

    def get_tier(self):
        project = DevelopmentProject.objects.filter(UnlocksModule=self)
        if project:
            return project[0].Tier
        return 0

    def is_module(self):
        if self.Features.all():
            return True
        return False

    def get_material_stacks(self):
        value = 0.0
        for input_material in self.InputMaterials.all():
            module = Module.objects.filter(Material=input_material.Material)
            if not module:
                value = value + (float(input_material.Amount) / float(input_material.Material.StackSize))
        return value

    def get_component_batches(self, do_recursive):
        value = 0.0
        for input_material in self.InputMaterials.all():
            module = Module.objects.filter(Material=input_material.Material)
            if module:
                if not module[0].is_module():
                    value = value + (float(input_material.Amount) / float(module[0].OutputAmount))
                    if do_recursive:
                        value = value + (module[0].get_component_batches(do_recursive) * (float(input_material.Amount) / float(module[0].OutputAmount)))
        return value

    def get_complexity(self):
        complexity = 0

        per_step = BalanceValue.objects.filter(Name="complexity_per_step")
        per_input = BalanceValue.objects.filter(Name="complexity_per_input")
        batch_factor = BalanceValue.objects.filter(Name="complexity_batch_factor")

        if per_step:
            complexity = float(complexity) + float(per_step[0].Value)

        for input_material in self.InputMaterials.all():
            if per_input:
                complexity = complexity + float(per_input[0].Value)

            module = Module.objects.filter(Material=input_material.Material)
            if module:
                batch_complexity = float(module[0].get_complexity())
                if batch_factor:
                    batch_complexity = batch_complexity * float(batch_factor[0].Value)
                batch_complexity = batch_complexity * (float(input_material.Amount) / float(module[0].OutputAmount))
                complexity = complexity + batch_complexity

        return complexity


    def rawMaterialCost(self):
        totalCost = 0
        for inputMat in self.InputMaterials.all():
            moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
            if moduleMatQuery.exists():
                if moduleMatQuery.all()[0].Name != self.Name:
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


class ProductTypeField(models.Model):
    productType = models.ForeignKey("ProductType", related_name="GridFields")
    x = models.IntegerField()
    y = models.IntegerField()

    def getJsonObject(self):
        return { "X" : self.x, "Y" : self.y }

    class Meta:
        verbose_name = 'Product Type Field'
        verbose_name_plural = 'Product Type Fields'

    def __unicode__(self):
        return u"%s GridFields" % (unicode(self.productType))

def ValidateMarketTier(tier):
    if tier <= 0:
        raise ValidationError("Market tiers must be greater than 0.")

class ProductType(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    ProductAssetID = models.CharField(max_length=255, default="")
    Description = models.CharField(max_length=255, blank=True)
    IconAssetID = models.CharField(max_length=255)
    BaseMarketPrice = models.IntegerField(default=100)
    BaseMarketDemand = models.IntegerField(default=10)
    RequiredDiscoveryPoints = models.IntegerField(default=10)
    MandatoryFeatures = models.ManyToManyField("ProductFeature")
    MarketTier = models.IntegerField(
        default=1,
        validators=[ValidateMarketTier],
        help_text="The market tier for this product type. "
            "This value must be greater than 0")


    def getJsonObject(self):

        gridfields = []
        for gridfield in self.GridFields.all():
            gridfields.append(gridfield.getJsonObject())
        cases = []
        for case in self.Cases.all():
            cases.append(case.getJsonObject())
        mandatoryFeatures = [feat.id for feat in self.MandatoryFeatures.all()]
        return {
            "Name": self.Name,
            "ProductAssetID": self.ProductAssetID,
            "Description": self.Description,
            "IconAssetID": self.IconAssetID,
            "BaseMarketPrice": self.BaseMarketPrice,
            "RequiredDiscoveryPoints": self.RequiredDiscoveryPoints,
            "PositiveFeatures": [],
            "NegativeFeatures": [],
            "MarketTier": self.MarketTier,
            "GridFields": gridfields,
            "Cases": cases,
            "MandatoryFeatures": mandatoryFeatures
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
    SymbolAssetID = models.CharField(max_length=255)
    HelperEmoji = models.CharField(max_length=4)
    PriceBonus = models.IntegerField(default=10)
    IsDrawback = models.BooleanField(default=False, help_text="This is a helper for the views, will get exported.")

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
            "SymbolAssetID": self.SymbolAssetID,
            "PriceBonus": self.PriceBonus,
            "IsDrawback": self.IsDrawback
        }

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'

    def __unicode__(self):
        return unicode(self.HelperEmoji + " " + self.Name)

class ProductTypeCase(models.Model):
    history = HistoricalRecords()
    ProductType = models.ForeignKey(ProductType, related_name="Cases")
    CaseModule = models.ForeignKey(Module, related_name="ProductTypesCase")

    def getJsonObject(self):
        blockingFields = []
        for blockingField in self.BlockingGridFields.all():
            blockingFields.append(blockingField.getJsonObject())
        return {
            "CaseModuleID": self.CaseModule.id,
            "BlockingFields": blockingFields,
        }

    class Meta:
        verbose_name = "Product Type Case"
        verbose_name_plural = "Product Type Cases"

    def __unicode__(self):
        return u"%s - %s" % (unicode(self.ProductType), unicode(self.CaseModule))


class ProductTypeCaseBlockingField(models.Model):
    ProductTypeCase = models.ForeignKey(ProductTypeCase, related_name="BlockingGridFields")
    X = models.IntegerField()
    Y = models.IntegerField()

    def getJsonObject(self):
        return {"X": self.X, "Y": self.Y}

    class Meta:
        verbose_name = 'Product Type Case blocking Field'
        verbose_name_plural = 'Product Type Case blocking Fields'

    def __unicode__(self):
        return u"%s blocking GridFields" % (unicode(self.ProductTypeCase))