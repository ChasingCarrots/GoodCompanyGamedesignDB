# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from Production.models import Module

def moduleOverview(request):
    modules = []
    for module in Module.objects.all():
        modules.append({
            "id": module.id,
            "name": module.Name,
            "matCost": module.rawMaterialCost(),
        })
    return render(request, "helpers/moduleoverview.html", {"modules": modules})

def moduleDetail(request, moduleID):
    module = get_object_or_404(Module, pk=moduleID)
    moduleBaseMaterials = module.collectMaterials()
    totalAmount = 0
    totalCost = 0
    for _, mat in moduleBaseMaterials.items():
        totalAmount += mat["amount"]
        totalCost += mat["totalcost"]

    moduleInputMaterials = []
    for moduleInputMat in module.InputMaterials.all():
        moduleInputMatModuleID = -1
        cost = moduleInputMat.Material.getPricePerUnit()
        moduleInputModuleQuery = Module.objects.filter(Material=moduleInputMat.Material)
        if moduleInputModuleQuery.exists():
            moduleInputModule = moduleInputModuleQuery.all()[0]
            moduleInputMatModuleID = moduleInputModule.id
            cost = moduleInputModule.rawMaterialCost()
        moduleInputMaterials.append({
            "name": moduleInputMat.Material.Name,
            "amount": moduleInputMat.Amount,
            "moduleID": moduleInputMatModuleID,
            "totalcost": cost * moduleInputMat.Amount,
        })
    return render(request, "helpers/moduledetail.html", {
        "module": {
            "name": module.Name,
            "inputMaterials": moduleInputMaterials,
        },
        "materials": moduleBaseMaterials,
        "total": {
            "amount": totalAmount,
            "totalcost": totalCost,
        },
    })
