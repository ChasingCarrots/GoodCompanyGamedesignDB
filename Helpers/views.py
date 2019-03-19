# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from helpers import *
from Helpers.balancing.modules import *
from Helpers.balancing.products import *

def productTypeOverview(request):
    productTypes = []
    for productType in ProductType.objects.all():
        productTypes.append({
            "id": productType.id,
            "name": productType.Name,
            "slotCount": productType.Slots.count(),
            "relevantModules": 0
        })
    return render(request, "helpers/producttypeoverview.html", {"productTypes": productTypes})

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
        moduleInputMatMaterialID = -1
        cost = moduleInputMat.Material.getPricePerUnit()
        moduleInputModuleQuery = Module.objects.filter(Material=moduleInputMat.Material)
        moduleInputMatMaterialID = moduleInputMat.Material.id
        if moduleInputModuleQuery.exists():
            moduleInputModule = moduleInputModuleQuery.all()[0]
            moduleInputMatModuleID = moduleInputModule.id
            cost = moduleInputModule.rawMaterialCost()
        moduleInputMaterials.append({
            "name": moduleInputMat.Material.Name,
            "amount": moduleInputMat.Amount,
            "moduleID": moduleInputMatModuleID,
            "materialID": moduleInputMatMaterialID,
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

def materialOverview(request):
    materials = []
    # get all materials
    for material in Material.objects.filter(module=None).all():
        materials.append({
            "id": material.id,
            "name": material.Name,
            "cost": material.getPricePerUnit(),
        })

    return render(request, "helpers/materialoverview.html", {"materials": materials})

def materialDetail(request, materialID):
    material = get_object_or_404(Material, pk=materialID)

    appliedValues = False
    if request.method == 'POST':
        failedSave = False
        try:
            material.StackSize = int(request.POST["stackSize"])
            material.StackBuyPrice = int(request.POST["stackPrice"])
            material.save()
        except Exception:
            failedSave = True
        appliedValues = not failedSave

    modules = material.collect_modules().values()

    detailInformation = {
        "material": {
            "name": material.Name,
            "id": material.id,
            "stackSize": material.StackSize,
            "stackPrice": material.StackBuyPrice,
            "unitPrice": material.getPricePerUnit(),
        },
        "modules": modules,
        "appliedValues": appliedValues,
    }
    
    return render(request, "helpers/materialdetail.html", detailInformation)

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

    interfaceNodesProperties = {}
    for interfaceNodes in InterfaceNodesProperty.objects.all():
        interfaceNodesProperties[str(interfaceNodes.ObjectType.id)] = interfaceNodes.getJsonObject()

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

    researchAndDevelopmentProperties = {}
    for rndProp in ResearchAndDevelopmentProperty.objects.all():
        researchAndDevelopmentProperties[str(rndProp.ObjectType.id)] = rndProp.getJsonObject()

    conveyorProperties = {}
    for convProp in ConveyorProperty.objects.all():
        conveyorProperties[str(convProp.ObjectType.id)] = convProp.getJsonObject()

    inventoryGroupProperties = {}
    for invgProp in InventoryGroupProperty.objects.all():
        inventoryGroupProperties[str(invgProp.ObjectType.id)] = invgProp.getJsonObject()

    tuningValues = {}
    for tuningValue in TuningValue.objects.all():
        tuningValues[tuningValue.Name] = tuningValue.getJsonValue()

    researchDataTypes = {}
    for researchData in ResearchDataType.objects.all():
        researchDataTypes[str(researchData.id)] = researchData.getJsonObject()

    developmentProjects = {}
    for devProj in DevelopmentProject.objects.all():
        developmentProjects[str(devProj.id)] = devProj.getJsonObject()

    return HttpResponse(json.dumps({
        "Materials": materials,
        "Modules": modules,
        "SlotTypes": slotTypes,
        "ProductTypes": productTypes,
        "ProductFeatures": productFeatures,
        "ProductFunctions": productFunctions,
        "ObjectTypes": objectTypes,
        "MovableProperties": movableProperties,
        "ObjectLookProperties": objectLookProperties,
        "IconProperties": iconProperties,
        "InventoryProperties": inventoryProperties,
        "StorageProperties": storageProperties,
        "BuildableProperties": buildableProperties,
        "RecurringCostProperties": recurringCostProperties,
        "CrafterProperties": crafterProperties,
        "AssemblyProperties": assemblyProperties,
        "InterfaceNodesProperties": interfaceNodesProperties,
        "StaticDimensionProperties": staticDimensionProperties,
        "InteractableTilesProperties": interactableTilesProperties,
        "SpecialFlagsProperties": specialFlagsProperties,
        "BlueprintPrinterProperties": blueprintPrinterProperties,
        "ResearchAndDevelopmentProperties": researchAndDevelopmentProperties,
        "ConveyorProperties": conveyorProperties,
        "InventoryGroupProperties": inventoryGroupProperties,
        "TuningValues": tuningValues,
        "ResearchDataTypes": researchDataTypes,
        "DevelopmentProjects": developmentProjects
    }, indent=4), content_type='application/json')

def revertChangesView(request):
    if request.method == "POST":
        year = int(request.POST["year"])
        month = int(request.POST["month"])
        day = int(request.POST["day"])
        hour = int(request.POST["hour"])
        minute = int(request.POST["minute"])
        pointInTime = timezone.make_aware(datetime(year, month, day, hour, minute))
        numReverted = revertChangesTo(pointInTime)
        return render(request, "helpers/revertchanges.html", {
            "message": "Success. Reverted %d Objects." % numReverted,
            "messageType": "success"
        })
    else:
        return render(request, "helpers/revertchanges.html")

def balancingTablesView(request):
    balancingTables = []
    for table in BalancingTableBase.__subclasses__():
        balancingTables.append(table.BalancingTableIdentifier)
    return render(request, "helpers/balancingtables.html", { "tables": balancingTables })

@csrf_exempt
def getBalancingTableJson(request, tablename, limitFrom, limitTo):
    for table in BalancingTableBase.__subclasses__():
        if tablename == table.BalancingTableIdentifier:
            balancingTable = table(int(limitFrom), int(limitTo))
            return HttpResponse(balancingTable.GetJson(), content_type='application/json')

    raise Http404()

@csrf_exempt
def setBalancingTableValue(request):
    for table in BalancingTableBase.__subclasses__():
        if request.POST["tablename"] == table.BalancingTableIdentifier:
            balancingTable = table(0,0)
            balancingTable.SetValueReceived(int(request.POST["column"]), int(request.POST["objID"]), request.POST["value"])
            return HttpResponse('{"result": "OK"}', content_type='application/json')

    return HttpResponse("{'result': 'FAIL'}", content_type='application/json')
