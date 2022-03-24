# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import Production
import common
from simple_history.models import HistoricalRecords
from bitfield import BitField
from Production.models import SkillType, Module

class ObjectType(models.Model):
    history = HistoricalRecords()
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description
        }

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = 'Object Type'
        verbose_name_plural = 'Object Types'
        ordering = ['id']


class MovableProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="MovableProperty", blank=False)
    Width = models.FloatField(default=0, blank=True)
    Height = models.FloatField(default=0, blank=True)
    Radius = models.FloatField(default=0, blank=True)

    def getJsonObject(self):
        movableJson = {}
        if self.Width != 0:
            movableJson["Width"] = self.Width
        if self.Height != 0:
            movableJson["Height"] = self.Height
        if self.Radius != 0:
            movableJson["Radius"] = self.Radius
        return movableJson

    class Meta:
        verbose_name = 'Movable Property'
        verbose_name_plural = 'Movable Properties'

    def __unicode__(self):
        return u"MovableProperty of %s" % (self.ObjectType)


class ObjectLookProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="ObjectLookProperty", blank=False)
    ModelAssetID = models.CharField(max_length=255, blank=False)
    CanChangeColor = models.BooleanField(default=False)

    def getJsonObject(self):
        return {
            "ModelAssetID": self.ModelAssetID,
            "CanChangeColor": self.CanChangeColor
        }

    class Meta:
        verbose_name = 'Object Look Property'
        verbose_name_plural = 'Object Look Properties'

    def __unicode__(self):
        return u"ObjectLookProperty of %s" % (self.ObjectType)


class IconProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="IconProperty", blank=False)
    IconAssetID = models.CharField(max_length=255, help_text="The asset id of the icon for this object.", blank=False)
    TextSpriteAssetID = models.CharField(max_length=255, help_text="The asset id of the TMP spritesheet that contains the text-sprite for this object.", blank=True)
    TextSpriteEntry = models.CharField(max_length=31, help_text="The name of the icon of this object within the TMP spritesheet", blank=True)

    def getJsonObject(self):
        return {
            "IconAssetID": self.IconAssetID,
            "TextSpriteAssetID": self.TextSpriteAssetID,
            "TextSpriteEntry": self.TextSpriteEntry,
        }

    class Meta:
        verbose_name = 'Icon Property'
        verbose_name_plural = 'Icon Properties'

    def __unicode__(self):
        return u"IconProperty of %s" % (self.ObjectType)

class InventoryProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="InventoryProperty", blank=False)
    SlotType = models.IntegerField(choices=common.SlotTypeChoices, blank=False)
    NumberOfSlots = models.IntegerField(blank=False)
    IsLogistic = models.BooleanField(default=False, blank=False, help_text="Only logistic inventories can be used in workplaces.")

    def getJsonObject(self):
        return {
            "SlotType": self.SlotType,
            "NumberOfSlots": self.NumberOfSlots,
            "IsLogistic": self.IsLogistic,
        }

    class Meta:
        verbose_name = 'Inventory Property'
        verbose_name_plural = 'Inventory Properties'

    def __unicode__(self):
        return u"InventoryProperty of %s" % (self.ObjectType)

class StorageProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="StorageProperty", blank=False)
    SizeType = models.IntegerField(choices=common.SizeTypeChoices, blank=False)
    ModelAssetID = models.CharField(max_length=255, help_text="The asset id of the model that should be used to display this object in an inventory view.", blank=True)

    def getJsonObject(self):
        return {
            "SizeType": self.SizeType,
            "ModelAssetID": self.ModelAssetID,
        }

    class Meta:
        verbose_name = 'Storage Property'
        verbose_name_plural = 'Storage Properties'

    def __unicode__(self):
        return u"StorageProperty of %s" % (self.ObjectType)

class BuildablePropertyNeededMaterial(models.Model):
    history = HistoricalRecords()
    BuildableProperty = models.ForeignKey("BuildableProperty", related_name="NeededMaterials", blank=False)
    Material = models.ForeignKey(Production.models.Material, blank=False)
    Amount = models.IntegerField(default=0)

    def getJsonObject(self):
        return {
            "MaterialID": self.Material.id,
            "Amount": self.Amount,
        }

    class Meta:
        verbose_name = 'NeededMaterial'
        verbose_name_plural = 'NeededMaterials'

    def __unicode__(self):
        return u"%s (%ds)" % (self.Material, self.Amount)


class BuildabelCategory(models.Model):
    Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255, blank=True)
    Order = models.IntegerField(default=1)
    Icon = models.CharField(max_length=255, null=True, blank=True)

    def getJsonObject(self):
        return {
            "Name": self.Name,
            "Description": self.Description,
            "IconAssetID": self.Icon,
            "Order": self.Order
        }

    class Meta:
        verbose_name = 'Buildable Category'
        verbose_name_plural = 'Buildable Categories'

    def __unicode__(self):
        return self.Name

class BuildableProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="BuildableProperty", blank=False)
    BuildDuration = models.FloatField(blank=False)
    Category = models.ForeignKey(BuildabelCategory, blank=True, null=True)
    OrderInCategory = models.IntegerField(default=1)
    MoneyCost = models.IntegerField(default=1000)
    CanBeBuiltOutdoors = models.BooleanField(default=False)
    MustBeBuiltInWorkzone = models.BooleanField(default=True)
    AddHappinessToWorkzone = models.FloatField(default=0)

    def getJsonObject(self):
        neededmats = []
        for mat in self.NeededMaterials.all():
            neededmats.append(mat.getJsonObject())
        category = 1
        if self.Category:
            category = self.Category.id
        return {
            "NeededMaterials": neededmats,
            "BuildDuration": self.BuildDuration,
            "Category": category,
            "BuildCost": self.MoneyCost,
            "OrderInCategory": self.OrderInCategory,
            "CanBeBuiltOutdoors": self.CanBeBuiltOutdoors,
            "MustBeBuiltInWorkzone": self.MustBeBuiltInWorkzone,
            "AddHappinessToWorkzone": self.AddHappinessToWorkzone
        }

    class Meta:
        verbose_name = 'Buildable Property'
        verbose_name_plural = 'Buildable Properties'

    def __unicode__(self):
        return u"BuildableProperty of %s" % (self.ObjectType)

    def materialCost(self):
        totalCost = 0
        for neededMat in self.NeededMaterials.all():
            totalCost += neededMat.Material.BuyPrice * neededMat.Amount
        return totalCost

class RecurringCostProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="RecurringCostProperty", blank=False)
    RecurringCost = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "RecurringCost":self.RecurringCost,
        }

    class Meta:
        verbose_name = 'RecurringCost Property'
        verbose_name_plural = 'RecurringCost Properties'

    def __unicode__(self):
        return u"RecurringCostProperty of %s" % (self.ObjectType)

class CrafterPropertyModuleDuration(models.Model):
    history = HistoricalRecords()
    CrafterProperty = models.ForeignKey("CrafterProperty", related_name="PossibleModules", blank=False)
    Module = models.ForeignKey(Production.models.Module, blank=False)
    Duration = models.FloatField(blank=False)
    BatchSize = models.IntegerField(default=1)

    def getJsonObject(self):
        return {
            "ModuleID": self.Module.id,
            "Duration": self.Duration,
            "BatchSize": self.BatchSize
        }

    class Meta:
        verbose_name = 'Possible Module'
        verbose_name_plural = 'Possible Modules'

    def __unicode__(self):
        return u"%s (%ds)" % (self.Module, self.Duration)

class CrafterProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="CrafterProperty", blank=False)
    SwitchingTime = models.FloatField(blank=False, default=1)
    Automatic = models.BooleanField(default=False, help_text="doesn't need an employee when set to true")
    AutomaticStorageMultiplier = models.IntegerField(default=10)

    def getJsonObject(self):
        possibleModules = [step.getJsonObject() for step in self.PossibleModules.all()]
        return {
            "SwitchingDuration": self.SwitchingTime,
            "PossibleModules": possibleModules,
            "Automatic": self.Automatic,
            "AutomaticStorageMultiplier": self.AutomaticStorageMultiplier
        }

    class Meta:
        verbose_name = 'Crafter Property'
        verbose_name_plural = 'Crafter Properties'

    def __unicode__(self):
        return u"CrafterProperty of %s" % (self.ObjectType)


class AssemblyPropertyProductTypeAssemblyDuration(models.Model):
    history = HistoricalRecords()
    AssemblyProperty = models.ForeignKey("AssemblyProperty", related_name="PossibleProductTypes", blank=False)
    ProductType = models.ForeignKey(Production.models.ProductType, blank=False)
    Duration = models.FloatField(blank=False)

    class Meta:
        verbose_name = 'Possible ProductType'
        verbose_name_plural = 'Possible ProductTypes'

    def __unicode__(self):
        return u"%s (%ds)" % (self.ProductType, self.Duration)

class AssemblyProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="AssemblyProperty", blank=False)

    def getJsonObject(self):
        productTypes = []
        for productType in self.PossibleProductTypes.all():
            productTypes.append({
                "ProductTypeID":productType.ProductType.id,
                "Duration":productType.Duration,
            })
        return {
            "ProductTypes": productTypes,
        }

    class Meta:
        verbose_name = 'Assembly Property'
        verbose_name_plural = 'Assembly Properties'

    def __unicode__(self):
        return u"AssemblyProperty of %s" % (self.ObjectType)

class InterfaceNodesProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="InterfaceNodesProperty", blank=False)

    def getJsonObject(self):
        interfaceNodes = []
        for node in self.InterfaceNodes.all():
            interfaceNodes.append({
                "X": node.XCoord,
                "Y": node.YCoord,
                "IsInput": node.IsInput,
            })
        return {
            "InterfaceNodes":interfaceNodes,
        }

    class Meta:
        verbose_name = "Interface Nodes Property"
        verbose_name_plural = "Interface Nodes Properties"

    def __unicode__(self):
        return u"InterfaceNodesProperty of %s" % (self.ObjectType)

class InterfaceNodesPropertyInterfaceNode(models.Model):
    history = HistoricalRecords()
    InterfaceNodesProperty = models.ForeignKey("InterfaceNodesProperty", related_name="InterfaceNodes", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)
    IsInput = models.BooleanField(blank=False)

    class Meta:
        verbose_name = 'Interface node'
        verbose_name_plural = 'Interface nodes'
    
    def __unicode__(self):
        return u"(%d, %d | %r)" % (self.XCoord, self.YCoord, self.IsInput)

class StaticDimensionPropertyBlockedTile(models.Model):
    history = HistoricalRecords()
    StaticDimensionProperty = models.ForeignKey("StaticDimensionProperty", related_name="BlockedTiles", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)

    class Meta:
        verbose_name = 'Blocked tile'
        verbose_name_plural = 'Blocked tiles'

    def __unicode__(self):
        return u"(%d, %d)" % (self.XCoord, self.YCoord)

class StaticDimensionProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="StaticDimensionProperty", blank=False)

    def getJsonObject(self):
        blockedTiles = []
        for tile in self.BlockedTiles.all():
            blockedTiles.append({
                "X": tile.XCoord,
                "Y": tile.YCoord,
            })
        return {
            "BlockedTiles":blockedTiles,
        }

    class Meta:
        verbose_name = 'StaticDimension Property'
        verbose_name_plural = 'StaticDimension Properties'

    def __unicode__(self):
        return u"StaticDimensionProperty of %s" % (self.ObjectType)


class InteractableTilesPropertyInteractableTile(models.Model):
    history = HistoricalRecords()
    InteractableTilesProperty = models.ForeignKey("InteractableTilesProperty", related_name="InteractableTiles", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)

    class Meta:
        verbose_name = 'Interactable tile'
        verbose_name_plural = 'Interactable tiles'

    def __unicode__(self):
        return u"(%d, %d)" % (self.XCoord, self.YCoord)


class InteractableTilesProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="InteractableTilesProperty", blank=False)

    def getJsonObject(self):
        interactableTiles = []
        for tile in self.InteractableTiles.all():
            interactableTiles.append({
                "X": tile.XCoord,
                "Y": tile.YCoord,
            })
        return {
            "InteractableTiles": interactableTiles,
        }

    class Meta:
        verbose_name = 'InteractableTiles Property'
        verbose_name_plural = 'InteractableTiles Properties'

    def __unicode__(self):
        return u"InteractableTilesProperty of %s" % (self.ObjectType)


class SpecialFlagsProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="SpecialFlagsProperty", blank=False)
    IsBuyPlace = models.BooleanField(default=False, blank=False)
    IsSellPlace = models.BooleanField(default=False, blank=False)
    IsInterfacePallet = models.BooleanField(default=False, blank=False)
    IsTrashCan = models.BooleanField(default=False, blank=False)
    IsDraftingTable = models.BooleanField(default=False, blank=False)
    IsContractBoard = models.BooleanField(default=False, blank=False, help_text="Contract boards allow the player to view and accept open contracts.")
    IsBatchEditor = models.BooleanField(default=False)
    IsPusher = models.BooleanField(default=False)
    IsPuller = models.BooleanField(default=False)
    IsMerger = models.BooleanField(default=False)
    IsSplitter = models.BooleanField(default=False)
    IsBuffer = models.BooleanField(default=False)
    IsUpgradeableShelf = models.BooleanField(default=False)

    def getJsonObject(self):
        return {
            "IsBuyPlace": self.IsBuyPlace,
            "IsSellPlace": self.IsSellPlace,
            "IsInterfacePallet": self.IsInterfacePallet,
            "IsTrashCan": self.IsTrashCan,
            "IsDraftingTable": self.IsDraftingTable,
            "IsContractBoard": self.IsContractBoard,
            "IsBatchEditor": self.IsBatchEditor,
            "IsPusher": self.IsPusher,
            "IsPuller": self.IsPuller,
            "IsMerger": self.IsMerger,
            "IsSplitter": self.IsSplitter,
            "IsBuffer": self.IsBuffer,
            "IsUpgradeableShelf": self.IsUpgradeableShelf
        }

    class Meta:
        verbose_name = 'SpecialFlags Property'
        verbose_name_plural = 'SpecialFlags Properties'

    def __unicode__(self):
        return u"SpecialFlagsProperty of %s" % (self.ObjectType)


class BlueprintPrinterProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="BlueprintPrinterProperty", blank=False)
    PrintingTime = models.FloatField(blank=False)
    NumberOfOutputSlots = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "PrintingTime": self.PrintingTime,
            "NumberOfOutputSlots": self.NumberOfOutputSlots,
        }

    class Meta:
        verbose_name = 'BlueprintPrinter Property'
        verbose_name_plural = 'BlueprintPrinter Properties'

    def __unicode__(self):
        return u"BlueprintPrinterProperty of %s" % (self.ObjectType)


class ResearchAndDevelopmentProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="ResearchAndDevelopmentProperty", blank=False)
    CanDoResearch = models.BooleanField(default=False, blank=False)
    CanDoDevelopment = models.BooleanField(default=False, blank=False)
    Speed = models.FloatField(default=1)
    PossibleModules = models.ManyToManyField(Module)

    def getJsonObject(self):
        possibleModules = [mod.id for mod in self.PossibleModules.all()]
        return {
            "CanDoResearch": self.CanDoResearch,
            "CanDoDevelopment": self.CanDoDevelopment,
            "Speed": self.Speed,
            "PossibleModules": possibleModules
        }

    class Meta:
        verbose_name = 'Research and Development Property'
        verbose_name_plural = 'Research and Development Properties'

    def __unicode__(self):
        return u"ResearchAndDevelopmentProperty of %s" % (self.ObjectType)

class InventoryGroupProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="InventoryGroupProperty", blank=False)
    SlotCapacity = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "SlotCapacity": self.SlotCapacity
        }
    
    class Meta:
        verbose_name = 'Inventory Group Property'
        verbose_name_plural = "Inventory Group Properties"

    def __unicode__(self):
        return u"InventoryGroupProperty of %s" % (self.ObjectType)

class ConveyorProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="ConveyorProperty", blank=False)
    IsConveyor = models.BooleanField(default=False, blank=False)
    IsRollerband = models.BooleanField(default=False, blank=False)
    IsOverhead = models.BooleanField(default=False, blank=False)

    def getJsonObject(self):
        return {
            "IsConveyor": self.IsConveyor,
            "IsRollerband": self.IsRollerband,
            "IsOverhead": self.IsOverhead,
        }

    class Meta:
        verbose_name = 'Conveyor Property'
        verbose_name_plural = 'Conveyor Properties'

    def __unicode__(self):
        return u"ConveyorProperty of %s" % (self.ObjectType)


class LogisticsWorkplaceProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="LogisticsWorkplaceProperty", blank=False)
    Reach = models.IntegerField(blank=False)

    def getJsonObject(self):
        return {
            "Reach": self.Reach
        }

    class Meta:
        verbose_name = 'Logistics Workplace Property'
        verbose_name_plural = "Logistics Workplace Properties"

    def __unicode__(self):
        return u"LogisticsWorkplaceProperty of %s" % (self.ObjectType)

class TransferTilesPropertyTile(models.Model):
    history = HistoricalRecords()
    TransferTilesProperty = models.ForeignKey("TransferTilesProperty", related_name="Tiles", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)
    PushDirections = BitField(flags=[
        "PositiveX",
        "PositiveY",
        "NegativeX",
        "NegativeY"
    ], default=0)
    ReceiveDirections = BitField(flags=[
        "PositiveX",
        "PositiveY",
        "NegativeX",
        "NegativeY"
    ], default=0)

    class Meta:
        verbose_name = 'Transfer tile'
        verbose_name_plural = 'Transfer tiles'

    def getJsonObject(self):
        return {
            "X": self.XCoord,
            "Y": self.YCoord,
            "PushDirections": int(self.PushDirections),
            "ReceiveDirections": int(self.ReceiveDirections)
        }

    def __unicode__(self):
        return u"(%d, %d)" % (self.XCoord, self.YCoord)


class TransferTilesProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="TransferTilesProperty", blank=False)

    def getJsonObject(self):
        return {
            "Tiles": [tile.getJsonObject() for tile in self.Tiles.all()]
        }

    class Meta:
        verbose_name = 'Transfer Tiles Property'
        verbose_name_plural = "Transfer Tiles Properties"

    def __unicode__(self):
        return u"TransferTilesProperty of %s" % (self.ObjectType)

class FlagTilesPropertyTile(models.Model):
    history = HistoricalRecords()
    FlagsTilesProperty = models.ForeignKey("FlagTilesProperty", related_name="Tiles", blank=False)
    XCoord = models.IntegerField(blank=False)
    YCoord = models.IntegerField(blank=False)
    Flags = BitField(flags=[
        "FloorTile",
        "ConveyorHatch",
        "BlockBuildable",
        "NeedsWallTile",
        "WallDecoration"
    ], default=0)

    class Meta:
        verbose_name = 'Flags tile'
        verbose_name_plural = 'Flags tiles'

    def getJsonObject(self):
        return {
            "X": self.XCoord,
            "Y": self.YCoord,
            "Flags": int(self.Flags)
        }

    def __unicode__(self):
        return u"(%d, %d)" % (self.XCoord, self.YCoord)

class FlagTilesProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="FlagTilesProperty", blank=False)

    def getJsonObject(self):
        return {
            "Tiles": [tile.getJsonObject() for tile in self.Tiles.all()]
        }

    class Meta:
        verbose_name = 'Flag Tiles Property'
        verbose_name_plural = "Flag Tiles Properties"

    def __unicode__(self):
        return u"FlagTilesProperty of %s" % (self.ObjectType)

class SkillRequirementsProperty(models.Model):
    history = HistoricalRecords()
    ObjectType = models.OneToOneField(ObjectType, related_name="SkillRequirementsProperty", blank=False)
    RequiredSkill = models.ForeignKey(SkillType, blank=False)

    def getJsonObject(self):
        return {
            "RequiredSkill": self.RequiredSkill.id
        }

    class Meta:
        verbose_name = 'Skill Requirements Property'
        verbose_name_plural = "Skill Requirements Properties"

    def __unicode__(self):
        return u"SkillRequirementsProperty of %s" % (self.ObjectType)