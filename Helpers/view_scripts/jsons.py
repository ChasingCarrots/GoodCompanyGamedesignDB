# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Production.models import *
from Research.models import *
from ObjectTypes.models import *

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def json_materials(request):
    materials = []
    for material in Material.objects.all().order_by("Name"):
        if Module.objects.filter(Material=material):
            module = Module.objects.filter(Material=material)[0]

            input_materials = []
            for input_material in ModuleInputMaterialAmount.objects.filter(Module=module):
                input_materials.append({
                    "material_id": input_material.Material.id,
                    "material_name": input_material.Material.Name,
                    "material_amount": input_material.Amount
                })

            module_features = []
            for module_feature in ModuleFeature.objects.filter(Module=module):
                module_features.append({
                    "feature_id": module_feature.ProductFeature.id,
                    "loca_string": module_feature.ProductFeature.Name,
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
                data_amounts.append({
                    "data_id": data_amount.ResearchDataType.id,
                    "loca_string": data_amount.ResearchDataType.Name,
                    "data_amount": data_amount.Amount
                })

            materials.append({
                "material_id": material.id,
                "module_id": module.id,
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
                "loca_string": material.Name,
                "stack_size": material.StackSize,
                "stack_buy_price": material.StackBuyPrice,
                "module_category": "cat_material"
            })

    return JsonResponse({"Materials": materials})
