# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Production.models import *
from BalancingHelper.models import *
from Research.models import *
from ObjectTypes.models import *

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def json_materials(request):
    version = "undefined"
    if BalanceValue.objects.filter(Name="version"):
        version = str(BalanceValue.objects.filter(Name="version")[0].Value)

    materials = []
    for material in Material.objects.all().order_by("Name"):
        icon = material.IconAssetID.split('/')


        if Module.objects.filter(Material=material):
            module = Module.objects.filter(Material=material)[0]

            input_materials = []
            for input_material in ModuleInputMaterialAmount.objects.filter(Module=module):
                material_icon = input_material.Material.IconAssetID.split('/')
                input_materials.append({
                    "material_id": input_material.Material.id,
                    "loca_string": input_material.Material.Name,
                    "icon_sprite": material_icon[0],
                    "icon_id": material_icon[1],
                    "material_amount": input_material.Amount
                })

            module_features = []
            for module_feature in ModuleFeature.objects.filter(Module=module):
                feature_icon = module_feature.ProductFeature.SymbolAssetID.split('/')
                module_features.append({
                    "feature_id": module_feature.ProductFeature.id,
                    "loca_string": module_feature.ProductFeature.Name,
                    "icon_sprite": feature_icon[0],
                    "icon_id": feature_icon[1],
                    "feature_value": module_feature.FeatureValue
                })

            module_fields = []
            for module_field in ModuleField.objects.filter(module=module):
                module_fields.append({
                    "x": module_field.x,
                    "y": module_field.y
                })

            data_amounts = []
            for data_amount in ModuleResearchDataYield.objects.filter(Module=module):
                data_icon = data_amount.ResearchDataType.IconAssetID.split('/')
                data_amounts.append({
                    "data_id": data_amount.ResearchDataType.id,
                    "loca_string": data_amount.ResearchDataType.Name,
                    "icon_sprite": data_icon[0],
                    "icon_id": data_icon[1],
                    "data_amount": data_amount.Amount
                })

            materials.append({
                "material_id": material.id,
                "module_id": module.id,
                "icon_sprite": icon[0],
                "icon_id": icon[1],
                "loca_string": material.Name,
                "stack_size": material.StackSize,
                "stack_buy_price": material.StackBuyPrice,
                "output_amount": module.OutputAmount,
                "sell_price": module.BaseMarketPrice,
                "assembly_time": module.AssemblyTime,
                "sampling_time": module.SamplingTime,
                "module_category": module.Category.Name,
                "order_in_category": module.OrderInCategory,
                "input_materials": input_materials,
                "module_features": module_features,
                "module_fields": module_fields,
                "data_amounts": data_amounts
            })
        else:
            materials.append({
                "material_id": material.id,
                "icon_sprite": icon[0],
                "icon_id": icon[1],
                "loca_string": material.Name,
                "stack_size": material.StackSize,
                "stack_buy_price": material.StackBuyPrice,
                "module_category": "cat_material"
            })

    return JsonResponse({"version": version, "materials": materials}, json_dumps_params={"indent": 4})


def json_techs(request):
    version = "undefined"
    if BalanceValue.objects.filter(Name="version"):
        version = str(BalanceValue.objects.filter(Name="version")[0].Value)

    techs = []
    for tech in DevelopmentProject.objects.order_by("Category", "OrderInCategory"):
        if tech.id > 60:
            icon = tech.IconAssetID.split('/')

            data_amounts = []
            for data_amount in DevelopmentProjectRequiredData.objects.filter(DevelopmentProject=tech):
                data_icon = data_amount.DataType.IconAssetID.split('/')
                data_amounts.append({
                    "data_id": data_amount.DataType.id,
                    "loca_string": data_amount.DataType.Name,
                    "icon_sprite": data_icon[0],
                    "icon_id": data_icon[1],
                    "data_amount": data_amount.Amount
                })

            required_techs = []
            for required_tech in DevelopmentProject.objects.filter(RequiredForProjects=tech):
                tech_icon = required_tech.IconAssetID.split('/')
                required_techs.append({
                    "tech_id": required_tech.id,
                    "loca_string": required_tech.Name,
                    "icon_sprite": tech_icon[0],
                    "icon_id": tech_icon[1],
                })

            module_list = []
            for module in Module.objects.filter(UnlockedByResearch=tech):
                module_icon = module.IconAssetID.split('/')
                module_list.append({
                    "module_id": module.id,
                    "loca_string": module.Name,
                    "icon_sprite": module_icon[0],
                    "icon_id": module_icon[1],
                })

            equipment_list = []
            for equipment in ObjectType.objects.filter(UnlockedByResearch=tech):
                icon = ["", ""]
                if IconProperty.objects.filter(ObjectType=equipment):
                    equip_icon = IconProperty.objects.filter(ObjectType=equipment)[0].IconAssetID.split('/')

                equipment_list.append({
                    "equipment_id": equipment.id,
                    "loca_string": equipment.Name,
                    "icon_sprite": equip_icon[0],
                    "icon_id": equip_icon[1],
                })

            techs.append({
                "tech_id": tech.id,
                "hidden_tech": tech.IsHidden,
                "icon_sprite": icon[0],
                "icon_id": icon[1],
                "loca_string": tech.Name,
                "tech_tier": tech.Tier,
                "tech_category": tech.Category.Name,
                "order_in_category": tech.OrderInCategory,
                "discovery_points": tech.DiscoveryPoints,
                "required_data": data_amounts,
                "required_techs": required_techs,
                "unlocked_modules": module_list,
                "unlocked_equipment": equipment_list
            })
    return JsonResponse({"version": version, "techs": techs}, json_dumps_params={"indent": 4})


def json_equipment(request):
    version = "undefined"
    if BalanceValue.objects.filter(Name="version"):
        version = str(BalanceValue.objects.filter(Name="version")[0].Value)

    equip_list = []
    for equip in ObjectType.objects.all():

        if equip.id > 2:
            icon = ["", ""]
            if IconProperty.objects.filter(ObjectType=equip):
                icon = IconProperty.objects.filter(ObjectType=equip)[0].IconAssetID.split('/')

            buildable_properties = []
            if BuildableProperty.objects.filter(ObjectType=equip):
                properties = BuildableProperty.objects.filter(ObjectType=equip)[0]

                material_list = []
                for material in BuildablePropertyNeededMaterial.objects.filter(BuildableProperty=properties):
                    material_icon = material.Material.IconAssetID.split('/')
                    material_list.append({
                        "material_id": material.Material.id,
                        "loca_string": material.Material.Name,
                        "icon_sprite": material_icon[0],
                        "icon_id": material_icon[1],
                        "material_amount": material.Amount
                    })

                buildable_properties.append({
                    "equipment_category": properties.Category.Name,
                    "order_in_category": properties.OrderInCategory,
                    "equipment_cost": properties.MoneyCost,
                    "can_be_built_outdoors": properties.CanBeBuiltOutdoors,
                    "materials": material_list
                })

            crafter_properties = []
            if CrafterProperty.objects.filter(ObjectType=equip):
                properties = CrafterProperty.objects.filter(ObjectType=equip)[0]

                module_list = []
                for module in CrafterPropertyModuleDuration.objects.filter(CrafterProperty=properties):
                    module_icon = module.Module.IconAssetID.split('/')
                    module_list.append({
                        "module_id": module.Module.id,
                        "loca_string": module.Module.Name,
                        "icon_sprite": module_icon[0],
                        "icon_id": module_icon[1],
                        "craft_duration": module.Duration,
                        "craft_batch": module.BatchSize,
                    })

                crafter_properties.append({
                    "automatic": properties.Automatic,
                    "crafting_list": module_list
                })

            assembly_properties = []
            if AssemblyProperty.objects.filter(ObjectType=equip):
                properties = AssemblyProperty.objects.filter(ObjectType=equip)[0]

                product_list = []
                for product in AssemblyPropertyProductTypeAssemblyDuration.objects.filter(AssemblyProperty=properties):
                    product_icon = product.ProductType.IconAssetID.split('/')
                    product_list.append({
                        "product_id": product.ProductType.id,
                        "loca_string": product.ProductType.Name,
                        "icon_sprite": product_icon[0],
                        "icon_id": product_icon[1],
                        "base_duration": product.Duration
                    })

                crafter_properties.append({
                    "crafting_list": product_list
                })

            inventory_properties = []
            if InventoryProperty.objects.filter(ObjectType=equip):
                properties = InventoryProperty.objects.filter(ObjectType=equip)[0]

                inventory_properties.append({
                    "inventory_slots": properties.NumberOfSlots
                })

            research_properties = []
            if ResearchAndDevelopmentProperty.objects.filter(ObjectType=equip):
                properties = ResearchAndDevelopmentProperty.objects.filter(ObjectType=equip)[0]

                research_properties.append({
                    "can_do_analysis": properties.CanDoResearch,
                    "can_do_research": properties.CanDoDevelopment,
                    "research_time": properties.Speed
                })


            equip_list.append({
                "equip_id": equip.id,
                "icon_sprite": icon[0],
                "icon_id": icon[1],
                "loca_string": equip.Name,
                "buildable_properties": buildable_properties,
                "crafter_properties": crafter_properties,
                "assembly_properties": assembly_properties,
                "research_properties": research_properties,
                "inventory_properties": inventory_properties
            })
    return JsonResponse({"version": version, "equipment": equip_list}, json_dumps_params={"indent": 4})