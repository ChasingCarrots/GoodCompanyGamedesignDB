# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Production.models import *
from Research.models import *
from ObjectTypes.models import *

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def module_details(request, module_id):
    module = get_object_or_404(Module, pk=module_id)

    rating_data = {}
    rating_data["features"] = 0
    rating_data["drawbacks"] = 0
    rating_data["fields"] = 0
    rating_data["cost"] = module.rawMaterialCost()
    rating_data["time"] = module.AssemblyTime

    data_table = []
    for data in module.ResearchDataYield.all():
        data_table.append({
            "id": data.ResearchDataType.id,
            "name": data.ResearchDataType.Name,
            "icon": data.ResearchDataType.IconAssetID,
            "amount": data.Amount,
            "value": data.ResearchDataType.NetWorth * data.Amount,
            "worth": data.ResearchDataType.NetWorth,
        })

    research_table = {}
    if DevelopmentProject.objects.filter(UnlocksModules=module):
        research = DevelopmentProject.objects.filter(UnlocksModules=module)[0]
        research_table = {
            "id": research.id,
            "samplingTime": module.SamplingTime,
            "data": data_table,
        }

    object_table = []
    for object in ObjectType.objects.filter(CrafterProperty__isnull=False).order_by("Name"):
        for possibleModule in object.CrafterProperty.PossibleModules.all():
            if possibleModule.Module == module:
                object_table.append({
                    "id": object.id,
                    "icon": object.IconProperty.IconAssetID,
                    "name": object.Name,
                    "totalTime": possibleModule.Duration,
                    "petItem": possibleModule.Duration / module.OutputAmount
                })

    features = []
    for feature in module.Features.filter(ProductFeature__IsDrawback="False").order_by("-FeatureValue"):
        rating_data["features"] += float(feature.FeatureValue) / 10.0
        features.append({
            "id": feature.ProductFeature.id,
            "name": feature.ProductFeature.Name,
            "emoji": feature.ProductFeature.HelperEmoji,
            "value": float(feature.FeatureValue) / 10.0
        })

    drawbacks = []
    for drawback in module.Features.filter(ProductFeature__IsDrawback="True").order_by("FeatureValue"):
        rating_data["drawbacks"] += float(drawback.FeatureValue) / 10.0
        drawbacks.append({
            "id": drawback.ProductFeature.id,
            "name": drawback.ProductFeature.Name,
            "emoji": drawback.ProductFeature.HelperEmoji,
            "value": float(drawback.FeatureValue) / 10.0
        })

    fields = []
    for field in module.GridFields.all():
        rating_data["fields"] += 1
        fields.append({
            "x": field.x,
            "y": field.y,
            "posx": field.x * 20 + 60,
            "posy": field.y * 20 - 10,
        })

    moduleBaseMaterials = module.collectMaterials()
    baseMaterialsAmount = 0
    baseMaterialCost = 0
    for _, mat in moduleBaseMaterials.items():
        baseMaterialsAmount += mat["amount"]
        baseMaterialCost += mat["totalcost"]

    moduleInputMaterials = []
    for moduleInputMat in module.InputMaterials.all():
        moduleInputMatModuleID = -1
        cost = moduleInputMat.Material.getPricePerUnit()
        moduleInputModuleQuery = Module.objects.filter(Material=moduleInputMat.Material)
        moduleInputMatMaterialID = moduleInputMat.Material.id
        if moduleInputModuleQuery.exists():
            moduleInputModule = moduleInputModuleQuery.all()[0]
            moduleInputMatModuleID = moduleInputModule.id
            cost = moduleInputModule.rawMaterialCost()
        moduleInputMaterials.append({
            "name": moduleInputMat.Material.Name,
            "icon": moduleInputMat.Material.IconAssetID,
            "amount": moduleInputMat.Amount / float(module.OutputAmount),
            "moduleID": moduleInputMatModuleID,
            "materialID": moduleInputMatMaterialID,
            "cost": cost * moduleInputMat.Amount / float(module.OutputAmount),
        })


    used_for_crafting = []
    recipe_count = 0
    for mod in Module.objects.all():
        if mod.InputMaterials.all().filter(Material=module.Material).exists():
            used_for_crafting.append({
                "id": mod.id,
                "name": mod.Name,
                "icon": mod.IconAssetID,
            })
            recipe_count += 1


    material_table = {
        "id": module.Material.id,
        "usedIn": used_for_crafting,
        "recipeCount": recipe_count,
        "stacksize": module.Material.StackSize
    }

    module_table = {
        "id": module.id,
        "name": module.Name,
        "icon": module.IconAssetID,
        "features": features,
        "drawbacks": drawbacks,
        "fields": fields,
        "baseMaterials": moduleBaseMaterials.items(),
        "baseMaterialsAmount": baseMaterialsAmount,
        "baseMaterialCost": baseMaterialCost,
        "inputMaterials": moduleInputMaterials,
        "outputAmount": module.OutputAmount,
        "sellPrice": module.BaseMarketPrice,
        "demand": module.BaseMarketCapacity,
        "category": module.Category.Name,
        "categoryOrder": module.OrderInCategory,
        "tags": module.Tags
    }

    rating_data["feat_cost"] = 0.0
    rating_data["rating_cost"] = 0.0
    if rating_data["cost"] > 0 and rating_data["features"] > 0:
        rating_data["feat_cost"] = rating_data["cost"] / (rating_data["features"] * 10)
        rating_data["rating_cost"] = ((1.0 - (rating_data["cost"] / (20.0 * rating_data["features"] * 10.0))) * 10.0) + 1.0

    rating_data["feat_drawbacks"] = 0.0
    rating_data["rating_drawbacks"] = 0.0
    if rating_data["drawbacks"] > 0 and rating_data["features"] > 0:
        rating_data["feat_drawbacks"] = rating_data["drawbacks"] / rating_data["features"]
        rating_data["rating_drawbacks"] = rating_data["features"] / rating_data["drawbacks"]

    rating_data["feat_fields"] = 0.0
    rating_data["rating_fields"] = 0.0
    if rating_data["fields"] > 0 and rating_data["features"] > 0:
        rating_data["feat_fields"] = rating_data["fields"] / (rating_data["features"] * 10)
        rating_data["rating_fields"] = rating_data["features"] * 10 / rating_data["fields"] * 1.5

    rating_data["feat_time"] = 0.0
    rating_data["rating_time"] = 0.0
    if rating_data["time"] > 0 and rating_data["features"] > 0:
        rating_data["feat_time"] = rating_data["time"] / (rating_data["features"] * 10)
        rating_data["rating_time"] = rating_data["features"] * 10 / rating_data["time"]

    rating_data["rating_total"] = 0
    rating_data["rating_total"] += rating_data["rating_time"] * 0.25
    rating_data["rating_total"] += rating_data["rating_fields"] * 0.25
    rating_data["rating_total"] += rating_data["rating_drawbacks"] * 0.25
    rating_data["rating_total"] += rating_data["rating_cost"] * 0.25

    return render(request, "helpers/moduledetail.html", {
        "module": module_table,
        "material": material_table,
        "research": research_table,
        "rating": rating_data,
        "objects": object_table
    })
    

    #featureValue = 0.0
    #drawbackValue = 0.0
    #moduleSize = 0.0

    #for feature in module.Features.all():
    #    if feature.ProductFeature.IsDrawback:
    #        drawbackValue = drawbackValue + feature.FeatureValue
    #    else:
    #        featureValue = featureValue + feature.FeatureValue

    #for field in module.GridFields.all():
    #    moduleSize = moduleSize + 1

    #moduleBaseMaterials = module.collectMaterials()
    #totalAmount = 0
    #totalCost = 0
    #for _, mat in moduleBaseMaterials.items():
    #    totalAmount += mat["amount"]
    #    totalCost += mat["totalcost"]

    #commands = []
    #for command in CommandBase.__subclasses__():
    #    commands.append(command.__name__)

    #moduleInputMaterials = []
    #for moduleInputMat in module.InputMaterials.all():
    #    moduleInputMatModuleID = -1
    #    cost = moduleInputMat.Material.getPricePerUnit()
    #    moduleInputModuleQuery = Module.objects.filter(Material=moduleInputMat.Material)
    #    moduleInputMatMaterialID = moduleInputMat.Material.id
    #    if moduleInputModuleQuery.exists():
    #        moduleInputModule = moduleInputModuleQuery.all()[0]
    #        moduleInputMatModuleID = moduleInputModule.id
    #        cost = moduleInputModule.rawMaterialCost()
    #    moduleInputMaterials.append({
    #        "name": moduleInputMat.Material.Name,
    #        "icon": moduleInputMat.Material.IconAssetID,
    #        "amount": moduleInputMat.Amount / float(module.OutputAmount),
    #        "moduleID": moduleInputMatModuleID,
    #        "materialID": moduleInputMatMaterialID,
    #        "totalcost": cost * moduleInputMat.Amount / float(module.OutputAmount),
    #    })

    #usedInModules = []
    #usedInModCount = 0
    #for mod in Module.objects.all():
    #    if mod.InputMaterials.all().filter(Material=module.Material).exists():
    #        usedInModules.append(mod)
    #        usedInModCount += 1

    #features = []
    #for feature in module.Features.all():
    #    features.append(feature)

    #tableList = []
    #_baseHandlingtime = 3.0
    #_handlingtimePerMaterial = 0.5
    #handlingCost = employeeCostPerSecond() * (
    #            len(module.InputMaterials.all()) * _handlingtimePerMaterial + _baseHandlingtime) / module.OutputAmount
    #employeeCostSlow = employeeCostPerSecond() * getComponentCraftingTime(module, _baseHandlingtime,
    #                                                                      _handlingtimePerMaterial, True, False, False)
    #employeeCostFast = employeeCostPerSecond() * getComponentCraftingTime(module, _baseHandlingtime,
    #                                                                      _handlingtimePerMaterial, True, True, False)

    #for object in ObjectType.objects.filter(CrafterProperty__isnull=False).order_by("Name"):
    #    for possibleModule in object.CrafterProperty.PossibleModules.all():
    #        if possibleModule.Module == module:
    #            productionCost = employeeCostPerSecond() * possibleModule.Duration / module.OutputAmount
    #            totalSlow = (productionCost + handlingCost + employeeCostSlow + module.rawMaterialCost())
    #            totalQuick = (productionCost + handlingCost + employeeCostFast + module.rawMaterialCost())
    #            tableList.append({
    #                "id": object.id,
    #                "name": object.Name,
    #                "productionTime": possibleModule.Duration / module.OutputAmount,
    #                "productionCost": productionCost,
    #                "productionRateSlow": 100 * productionCost / totalSlow,
    #                "productionRateQuick": 100 * productionCost / totalQuick,
    #                "handlingRateSlow": 100 * handlingCost / totalSlow,
    #                "handlingRateQuick": 100 * handlingCost / totalQuick,
    #                "preStepRateSlow": 100 * employeeCostSlow / totalSlow,
    #                "preStepRateQuick": 100 * employeeCostFast / totalQuick,
    #                "materialRateSlow": 100 * module.rawMaterialCost() / totalSlow,
    #                "materialRateQuick": 100 * module.rawMaterialCost() / totalQuick,
    #                "totalCostSlow": totalSlow,
    #                "totalCostQuick": totalQuick,
    #            })

    #criticalModule = ModulePathObject.objects.all().filter(Module=module)
    #criticalPath = {}
    #if criticalModule:
    #    criticalPath["position"] = criticalModule[0].PathPosition
    #    criticalPath["expectedPosition"] = criticalModule[0].getExpectedPathPosition()
    #    criticalPath["id"] = criticalModule[0].Path.id
    #    criticalPath["name"] = criticalModule[0].Path.Name
    #    criticalPath["progression"] = criticalModule[0].getProgressionPoint()
    #    criticalPath["mainFeature"] = criticalModule[0].Path.MainFeature
    #    criticalPath["positiveFeatures"] = criticalModule[0].Path.PositiveFeatures.all()
    #    criticalPath["negativeFeatures"] = criticalModule[0].Path.NegativeFeatures.all()
    #    criticalPath["initialCosts"] = criticalModule[0].getExpectedInitialCosts()
    #    criticalPath["minimumCosts"] = criticalModule[0].getExpectedMinimumCosts()
    #    criticalPath["sellPrice"] = criticalModule[0].getExpectedSellPrice()

    #totalTime = getComponentCraftingTime(module, 0, 0, False, False) + module.AssemblyTime
    #featureRating = 0.0
    #if module.rawMaterialCost() > 0:
    #    featureRating = (featureValue/module.rawMaterialCost())*5.0
    #drawbackRating = 0.0
    #if drawbackValue > 0:
    #    drawbackRating = (float(featureValue)/float(drawbackValue))
    #sizeRating = 0.0
    #if moduleSize > 0:
    #    sizeRating = (featureValue/moduleSize)*3.0
    #timeRating = 0.0
    #if totalTime > 0:
    #    timeRating = (featureValue/totalTime)*1.0
    #totalRating = (featureRating + featureRating + drawbackRating + sizeRating + timeRating) * 0.2

    #return render(request, "helpers/moduledetail.html", {
    #    "module": {
    #        "name": module.Name,
    #        "inputMaterials": moduleInputMaterials,
    #        "features": features,
    #        "icon": module.IconAssetID,
    #        "id": module.id,
    #        "materialId": module.Material.id,
    #        "complexity": getComponentComplexity(module),
    #        "costs": totalCostPerComponent(module, 0),
    #        "materialcosts": module.rawMaterialCost(),
    #        "profit": totalProfitPerComponent(module, 0),
    #        "income": module.BaseMarketPrice,
    #        "profitability": getComponentProfitability(module, 0),
    #        "craftingTime": getComponentCraftingTime(module, 0, 0, False, False),
    #        "perMinuteRate": componentsPerSecond(module, 0) * 60,
    #        "perMinuteProfit": componentProfitPerSecond(module, 0) * 60,
    #        "outputAmount": module.OutputAmount,
    #        "usedinmodulescount": usedInModCount,
    #        "handlingCost": handlingCost,
    #        "employeeCostSlow": employeeCostSlow,
    #        "employeeCostQuick": employeeCostFast,
    #    },
    #    "balancing": {
    #        "totalRating": totalRating,
    #        "featureRating": featureRating,
    #        "drawbackRating": drawbackRating,
    #        "sizeRating": sizeRating,
    #        "timeRating": timeRating,
    #        "featureCount": featureValue,
    #        "materialCosts": module.rawMaterialCost(),
    #        "drawbackCount": drawbackValue,
    #        "moduleSize": moduleSize,
    #        "totalTime": totalTime,
    #    },
    #    "tableList": tableList,
    #    "criticalPath": criticalPath,
    #    "materials": moduleBaseMaterials,
    #    "usedinmodules": usedInModules,
    #    "total": {
    #        "amount": totalAmount,
    #        "totalcost": totalCost,
    #    },
    #    "commands": commands,
    #})