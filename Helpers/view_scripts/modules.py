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

    research_table = {}
    if DevelopmentProject.objects.filter(UnlocksModules=module):
        research = DevelopmentProject.objects.filter(UnlocksModules=module)[0]
        research_table = {
            "id": research.id,
            "samplingTime": module.SamplingTime,
            "data": get_module_datayield(module),
            "tier": research.Tier
        }

    base_materials = module.collectMaterials()
    base_amount = 0
    base_cost = 0
    for _, mat in base_materials.items():
        base_amount += mat["amount"]
        base_cost += mat["totalcost"]

    material_table = {
        "id": module.Material.id,
        "usedIn": get_module_usedin(module),
        "stacksize": module.Material.StackSize
    }

    module_table = {
        "id": module.id,
        "name": module.Name,
        "icon": module.IconAssetID,
        "features": get_module_features(module),
        "drawbacks": get_module_drawbacks(module),
        "fields": get_module_fields(module, 20, 60, 10),
        "baseMaterials": base_materials.items(),
        "baseMaterialsAmount": base_amount,
        "complexity": module.get_complexity(),
        "baseMaterialCost": base_cost,
        "inputMaterials": get_input_materials(module),
        "outputAmount": module.OutputAmount,
        "sellPrice": module.BaseMarketPrice,
        "demand": module.BaseMarketCapacity,
        "category": module.Category.Name,
        "categoryOrder": module.OrderInCategory,
        "tags": module.Tags,
    }

    return render(request, "helpers/moduledetail.html", {
        "module": module_table,
        "material": material_table,
        "research": research_table,
        "rating": get_module_rating(module),
        "objects": get_module_tables(module)
    })


def module_overview(request):
    categories = []
    for cat in ModuleCategory.objects.all().order_by("Order"):
        modules = []
        for module in Module.objects.filter(Category=cat).order_by("OrderInCategory"):
            modules.append(module)
        categories.append({
            "id": cat.id,
            "name": cat.Name,
            "order": cat.Order,
            "modules": modules
        })

    return render(request, "helpers/moduleoverview.html", {"categories": categories})


def module_category(request, category_id):
    category = get_object_or_404(ModuleCategory, pk=category_id)

    category_table = {
        "id": category.id,
        "name": category.Name
    }


    module_list = []
    for module in Module.objects.filter(Category=category).order_by("OrderInCategory"):
        researchid = False
        if DevelopmentProject.objects.filter(UnlocksModules=module):
            researchid = DevelopmentProject.objects.filter(UnlocksModules=module)[0].id
            tier = DevelopmentProject.objects.filter(UnlocksModules=module)[0].Tier

        base_materials = module.collectMaterials()
        base_amount = 0
        base_cost = 0
        for _, mat in base_materials.items():
            base_amount += mat["amount"]
            base_cost += mat["totalcost"]

        module_list.append({
            "id": module.id,
            "material": module.Material.id,
            "research": researchid,
            "name": module.Name,
            "tier": tier,
            "complexity": module.get_complexity(),
            "order": module.OrderInCategory,
            "icon": module.IconAssetID,
            "fields": get_module_fields(module, 15, 30, 7),
            "rating": get_module_rating(module),
            "features": get_module_features(module),
            "conversion": get_module_conversion(module),
            "drawbacks": get_module_drawbacks(module),
            "outputAmount": module.OutputAmount,
            "sellPrice": module.BaseMarketPrice,
            "demand": module.BaseMarketCapacity,
            "category": module.Category.Name,
            "categoryOrder": module.OrderInCategory,
            "tags": module.Tags,
            "stacksize": module.Material.StackSize,
            "samplingTime": module.SamplingTime,
            "data": get_module_datayield(module),
            "baseMaterials": base_materials.items(),
            "baseMaterialsAmount": base_amount,
            "baseMaterialCost": base_cost,
        })

    return render(request, "helpers/modulecategory.html", {
        "category": category_table,
        "modules": module_list
    })


def get_module_tables(module):
    object_table = []
    for obj in ObjectType.objects.filter(CrafterProperty__isnull=False).order_by("Name"):
        for possibleModule in obj.CrafterProperty.PossibleModules.all():
            if possibleModule.Module == module:
                object_table.append({
                    "id": obj.id,
                    "icon": obj.IconProperty.IconAssetID,
                    "name": obj.Name,
                    "totalTime": possibleModule.Duration,
                    "petItem": possibleModule.Duration / module.OutputAmount
                })
    return object_table


def get_module_datayield(module):
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
    return data_table


def get_input_materials(module):
    module_input_materials = []
    for module_input_mat in module.InputMaterials.all():
        module_id = -1
        cost = module_input_mat.Material.getPricePerUnit()
        query = Module.objects.filter(Material=module_input_mat.Material)
        material_id = module_input_mat.Material.id
        if query.exists():
            module = query.all()[0]
            module_id = module.id
            cost = module.rawMaterialCost()
        module_input_materials.append({
            "name": module_input_mat.Material.Name,
            "icon": module_input_mat.Material.IconAssetID,
            "amount": module_input_mat.Amount / float(module.OutputAmount),
            "moduleID": module_id,
            "materialID": material_id,
            "cost": cost * module_input_mat.Amount / float(module.OutputAmount),
        })
    return module_input_materials


def get_module_usedin(module):
    used_for_crafting = []
    for mod in Module.objects.all():
        if mod.InputMaterials.all().filter(Material=module.Material).exists():
            used_for_crafting.append({
                "id": mod.id,
                "name": mod.Name,
                "icon": mod.IconAssetID,
            })
    return used_for_crafting


def get_module_features(module):
    features = []
    for feature in module.Features.filter(ProductFeature__IsDrawback="False").order_by("-FeatureValue"):
        if float(feature.FeatureValue) > 0:
            features.append({
                "id": feature.ProductFeature.id,
                "name": feature.ProductFeature.Name,
                "emoji": feature.ProductFeature.HelperEmoji,
                "value": float(feature.FeatureValue) / 10.0
            })
    return features


def get_module_conversion(module):
    features = []
    for feature in module.Features.filter(ProductFeature__IsDrawback="False").order_by("-FeatureValue"):
        if float(feature.FeatureValue) < 0:
            features.append({
                "id": feature.ProductFeature.id,
                "name": feature.ProductFeature.Name,
                "emoji": feature.ProductFeature.HelperEmoji,
                "value": float(feature.FeatureValue) / 10.0
            })
    return features


def get_module_drawbacks(module):
    drawbacks = []
    for drawback in module.Features.filter(ProductFeature__IsDrawback="True").order_by("FeatureValue"):
        drawbacks.append({
            "id": drawback.ProductFeature.id,
            "name": drawback.ProductFeature.Name,
            "emoji": drawback.ProductFeature.HelperEmoji,
            "value": float(drawback.FeatureValue) / 10.0
        })
    return drawbacks


def get_module_fields(module, size, x, y):
    fields = []
    for field in module.GridFields.all():
        fields.append({
            "x": field.x,
            "y": field.y,
            "posx": field.x * size + x,
            "posy": field.y * size - y,
        })
    return fields


def get_module_rating(module):
    rating_data = {}
    rating_data["features"] = 0
    rating_data["drawbacks"] = 0
    rating_data["fields"] = 0
    rating_data["cost"] = module.rawMaterialCost()
    rating_data["time"] = module.AssemblyTime
    rating_data["conversion"] = 0

    for feature in module.Features.filter(ProductFeature__IsDrawback="False").order_by("-FeatureValue"):
        if float(feature.FeatureValue) > 0:
            rating_data["features"] += float(feature.FeatureValue) / 10.0
        else:
            rating_data["conversion"] -= float(feature.FeatureValue) / 10.0

    if rating_data["conversion"] > 0:
        rating_data["conversation_rate"] = rating_data["features"] / rating_data["conversion"]
    else:
        rating_data["conversation_rate"] = 0

    for drawback in module.Features.filter(ProductFeature__IsDrawback="True").order_by("FeatureValue"):
        rating_data["drawbacks"] += float(drawback.FeatureValue) / 10.0

    for field in module.GridFields.all():
        rating_data["fields"] += 1

    rating_calculation_costs = str(BalanceValue.objects.filter(Name="rating_calculation_costs")[0].Value)
    rating_calculation_costs = rating_calculation_costs.replace("$cost", "rating_data[\"feat_cost\"]")
    rating_data["feat_cost"] = 0.0
    rating_data["rating_cost"] = 0.0
    if rating_data["cost"] > 0 and rating_data["features"] > 0:
        rating_data["feat_cost"] = rating_data["cost"] / (rating_data["features"] * 10)
        rating_data["rating_cost"] = eval(rating_calculation_costs)

    rating_calculation_drawback = str(BalanceValue.objects.filter(Name="rating_calculation_drawback")[0].Value)
    rating_calculation_drawback = rating_calculation_drawback.replace("$drawbacks", "rating_data[\"feat_drawbacks\"]")
    rating_data["feat_drawbacks"] = 0.0
    rating_data["rating_drawbacks"] = 0.0
    if rating_data["drawbacks"] > 0 and rating_data["features"] > 0:
        rating_data["feat_drawbacks"] = rating_data["drawbacks"] / rating_data["features"]
        rating_data["rating_drawbacks"] = eval(rating_calculation_drawback)

    rating_calculation_fields = str(BalanceValue.objects.filter(Name="rating_calculation_fields")[0].Value)
    rating_calculation_fields = rating_calculation_fields.replace("$features", "rating_data[\"features\"]")
    rating_calculation_fields = rating_calculation_fields.replace("$fields", "rating_data[\"fields\"]")
    rating_data["feat_fields"] = 0.0
    rating_data["rating_fields"] = 0.0
    if rating_data["fields"] > 0 and rating_data["features"] > 0:
        rating_data["feat_fields"] = rating_data["fields"] / (rating_data["features"] * 10)
        rating_data["rating_fields"] = eval(rating_calculation_fields)

    rating_calculation_time = str(BalanceValue.objects.filter(Name="rating_calculation_time")[0].Value)
    rating_calculation_time = rating_calculation_time.replace("$features", "rating_data[\"features\"]")
    rating_calculation_time = rating_calculation_time.replace("$time", "rating_data[\"time\"]")
    rating_data["feat_time"] = 0.0
    rating_data["rating_time"] = 0.0
    if rating_data["time"] > 0 and rating_data["features"] > 0:
        rating_data["feat_time"] = rating_data["time"] / (rating_data["features"] * 10.0)
        rating_data["rating_time"] = eval(rating_calculation_time)

    rating_data["rating_total"] = 0
    rating_data["rating_total"] += rating_data["rating_time"] * 0.25
    rating_data["rating_total"] += rating_data["rating_fields"] * 0.25
    rating_data["rating_total"] += rating_data["rating_drawbacks"] * 0.25
    rating_data["rating_total"] += rating_data["rating_cost"] * 0.25

    return rating_data