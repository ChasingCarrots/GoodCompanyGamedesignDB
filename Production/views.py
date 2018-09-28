# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse

from Production.models import *
from ObjectTypes.models import *
from Tuning.models import TuningValue

def getManifestJson(request):
    materials = {}
    for mat in Material.objects.all():
        materials[str(mat.id)] = mat.getJsonObject()

    modules = {}
    for mod in Module.objects.all():
        modules[str(mod.id)] = mod.getJsonObject()

    slotTypes = {}
    for slotType in ModuleSlotType.objects.all():
        slotTypes[str(slotType.id)] = slotType.getJsonObject()

    productTypes = {}
    for productType in ProductType.objects.all():
        productTypes[str(productType.id)] = productType.getJsonObject()
    
    productFeatures = {}
    for productFeature in ProductFeature.objects.all():
        productFeatures[str(productFeature.id)] = productFeature.getJsonObject()

    productFunctions = {}
    for prodFunc in ProductFunction.objects.all():
        productFunctions[str(prodFunc.id)] = prodFunc.getJsonObject()

    objectTypes = {}
    for objectType in ObjectType.objects.all():
        objectTypes[str(objectType.id)] = objectType.getJsonObject()
        
    movableProperties = {}
    for movable in MovableProperty.objects.all():
        movableProperties[str(movable.ObjectType.id)] = movable.getJsonObject()

    objectLookProperties = {}
    for objectLook in ObjectLookProperty.objects.all():
        objectLookProperties[str(objectLook.ObjectType.id)] = objectLook.getJsonObject()

    iconProperties = {}
    for icon in IconProperty.objects.all():
        iconProperties[str(icon.ObjectType.id)] = icon.getJsonObject()

    inventoryProperties = {}
    for inventory in InventoryProperty.objects.all():
        inventoryProperties[str(inventory.ObjectType.id)] = inventory.getJsonObject()

    storageProperties = {}
    for storage in StorageProperty.objects.all():
        storageProperties[str(storage.ObjectType.id)] = storage.getJsonObject()

    buildableProperties = {}
    for buildable in BuildableProperty.objects.all():
        buildableProperties[str(buildable.ObjectType.id)] = buildable.getJsonObject()

    recurringCostProperties = {}
    for recurringCost in RecurringCostProperty.objects.all():
        recurringCostProperties[str(recurringCost.ObjectType.id)] = recurringCost.getJsonObject()

    crafterProperties = {}
    for crafter in CrafterProperty.objects.all():
        crafterProperties[str(crafter.ObjectType.id)] = crafter.getJsonObject()

    assemblyProperties = {}
    for assembly in AssemblyProperty.objects.all():
        assemblyProperties[str(assembly.ObjectType.id)] = assembly.getJsonObject()

    staticDimensionProperties = {}
    for staticDimension in StaticDimensionProperty.objects.all():
        staticDimensionProperties[str(staticDimension.ObjectType.id)] = staticDimension.getJsonObject()

    interactableTilesProperties = {}
    for interactableTiles in InteractableTilesProperty.objects.all():
        interactableTilesProperties[str(interactableTiles.ObjectType.id)] = interactableTiles.getJsonObject()

    specialFlagsProperties = {}
    for specialFlags in SpecialFlagsProperty.objects.all():
        specialFlagsProperties[str(specialFlags.ObjectType.id)] = specialFlags.getJsonObject()

    blueprintPrinterProperties = {}
    for blueprintPrinter in BlueprintPrinterProperty.objects.all():
        blueprintPrinterProperties[str(blueprintPrinter.ObjectType.id)] = blueprintPrinter.getJsonObject()

    tuningValues = {}
    for tuningValue in TuningValue.objects.all():
        tuningValues[tuningValue.Name] = tuningValue.getJsonValue()

    return HttpResponse(json.dumps({
        "Materials":materials,
        "Modules":modules,
        "SlotTypes":slotTypes,
        "ProductTypes":productTypes,
        "ProductFeatures":productFeatures,
        "ProductFunctions":productFunctions,
        "ObjectTypes":objectTypes,
        "MovableProperties": movableProperties,
        "ObjectLookProperties": objectLookProperties,
        "IconProperties": iconProperties,
        "InventoryProperties": inventoryProperties,
        "StorageProperties": storageProperties,
        "BuildableProperties": buildableProperties,
        "RecurringCostProperties": recurringCostProperties,
        "CrafterProperties": crafterProperties,
        "AssemblyProperties": assemblyProperties,
        "StaticDimensionProperties": staticDimensionProperties,
        "InteractableTilesProperties": interactableTilesProperties,
        "SpecialFlagsProperties": specialFlagsProperties,
        "BlueprintPrinterProperties": blueprintPrinterProperties,
        "TuningValues": tuningValues
    }, indent=4), content_type='application/json')
