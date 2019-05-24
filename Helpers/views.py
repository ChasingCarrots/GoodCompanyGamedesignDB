# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from helpers import *
from balancing.modules import *
from balancing.products import *
from commands.sanitychecks import *
from commands.tempcommands import *

def productTypeOverview(request):
    productTypes = []
    for productType in ProductType.objects.all():

        moduleCount = 0
        for slot in productType.Slots.all():
            moduleQuery = Module.objects.filter(FitsIntoSlot=slot)
            if moduleQuery.exists():
                moduleCount += len(moduleQuery)

        functionCount = 0
        functionQuery = ProductFunction.objects.filter(ViableProductTypes=productType)
        if functionQuery.exists():
            functionCount += len(functionQuery)

        productTypes.append({
            "id": productType.id,
            "name": productType.Name,
            "slotCount": productType.Slots.count(),
            "icon": productType.IconAssetID,
            "functions": functionCount,
            "relevantModules": moduleCount
        })
    return render(request, "helpers/producttypeoverview.html", {"productTypes": productTypes})


def productTypeDetail(request, typeID):

    productType = get_object_or_404(ProductType, pk=typeID)
    productSlots = []
    modules = []
    functions = []
    samples = []

    moduleCount = 0
    functionCount = 0

    for slot in productType.Slots.all():
        productSlots.append({
            "id": slot.id,
            "name": slot.Name,
            "isOptional": slot.IsOptional
        })
        moduleQuery = Module.objects.filter(FitsIntoSlot=slot)
        for module in moduleQuery.all():
            moduleCount += 1
            modules.append({
                "slot": slot.id,
                "id": module.id,
                "name": module.Name,
                "icon": module.IconAssetID,
            })

    functionQuery = ProductFunction.objects.filter(ViableProductTypes=productType)
    for function in functionQuery.all():
        functionCount += 1
        functions.append({
            "id": function.id,
            "name": function.Name,
            "icon": function.IconAssetID,
            "price": function.BaseMarketPrice
        })
        sampleQuery = SampleProduct.objects.filter(ProductFunction=function)
        for sample in sampleQuery.all():
            samples.append({
                "function": function.id,
                "id": sample.id,
                "name": sample.Name
            })




    return render(request, "helpers/producttypedetail.html", {
        "productType": {
            "id": productType.id,
            "name": productType.Name,
            "icon": productType.IconAssetID,
            "slotCount": productType.Slots.count(),
            "functionCound": functionCount,
            "moduleCount": moduleCount,
            "slots": productSlots,
            "modules": modules,
            "functions": functions,
            "samples": samples
        }
    })


def sampleProduct(request, productId):
    product = get_object_or_404(SampleProduct, pk=productId)

    totalAmount = 0
    totalCost = 0
    moduleBaseMaterials = product.collectMaterials()

    for _, mat in moduleBaseMaterials.items():
        totalAmount += mat["amount"]
        totalCost += mat["totalcost"]

    modules = []
    moduleCount = 0

    for module in product.Modules.all():
        modules.append({
            "name": module.Name,
            "icon": module.IconAssetID,
            "id": module.id,
            "materialId": module.Material.id,
            "complexity": getComponentComplexity(module),
            "costs": totalCostPerComponent(module, 0),
            "profit": totalProfitPerComponent(module, 0),
            "income": module.BaseMarketPrice,
            "profitability": getComponentProfitability(module, 0),
            "craftingTime": getComponentCraftingTime(module, 0, False),
            "perMinuteRate": componentsPerSecond(module, 0) * 60,
            "perMinuteProfit": componentProfitPerSecond(module, 0) * 60,
            "outputAmount": module.OutputAmount,
        })

    commands = []
    for command in CommandBase.__subclasses__():
        commands.append(command.__name__)

    return render(request, "helpers/sampleproduct.html", {
        "product": {
            "id": product.id,
            "name": product.Name,
            "function": product.ProductFunction.id,
            "icon": product.ProductFunction.IconAssetID,
            "costsMaterial": materialCostPerProduct(product),
            "costsEmployees": employeeCostPerProduct(product, 0),
            "costs": totalCostPerProduct(product, 0),
            "profit": totalProfitPerProduct(product, 0),
            "profitability": getProductProfitability(product, 0),
            "income": product.ProductFunction.BaseMarketPrice,
            "moduleValue": getProductModuleValue(product),
            "moduleValueDifference": product.ProductFunction.BaseMarketPrice - getProductModuleValue(product),
            "craftingTime": getProductCraftingTime(product,0,False),
            "perMinuteRate": productCostsPerSecond(product, 0) * 60,
            "perMinuteProfit": productProfitPerSecond(product, 0) * 60,
            "complexity": getProductComplexity(product, True),
            "moduleCount": moduleCount,
            "modules": modules
        },
        "materials": moduleBaseMaterials,
        "total": {
            "amount": totalAmount,
            "totalcost": totalCost,
        },
        "commands": commands,
    })

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

    commands = []
    for command in CommandBase.__subclasses__():
        commands.append(command.__name__)

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
            "icon": moduleInputMat.Material.IconAssetID,
            "amount": moduleInputMat.Amount,
            "moduleID": moduleInputMatModuleID,
            "materialID": moduleInputMatMaterialID,
            "totalcost": cost * moduleInputMat.Amount,
        })
    return render(request, "helpers/moduledetail.html", {
        "module": {
            "name": module.Name,
            "inputMaterials": moduleInputMaterials,
            "icon": module.IconAssetID,
            "id": module.id,
            "materialId": module.Material.id,
            "complexity": getComponentComplexity(module),
            "costs": totalCostPerComponent(module, 0),
            "profit": totalProfitPerComponent(module, 0),
            "income": module.BaseMarketPrice,
            "profitability": getComponentProfitability(module, 0),
            "craftingTime": getComponentCraftingTime(module, 0, False),
            "perMinuteRate": componentsPerSecond(module, 0) * 60,
            "perMinuteProfit": componentProfitPerSecond(module, 0) * 60,
            "outputAmount": module.OutputAmount,
        },
        "materials": moduleBaseMaterials,
        "total": {
            "amount": totalAmount,
            "totalcost": totalCost,
        },
        "commands": commands,
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
            "icon": material.IconAssetID,
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

    logisticsWorkplaces = {}
    for logWork in LogisticsWorkplaceProperty.objects.all():
        logisticsWorkplaces[str(logWork.ObjectType.id)] = logWork.getJsonObject()

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
        "LogisticsWorkplaceProperties": logisticsWorkplaces,
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
        balancingTables.append(table.__name__)
    return render(request, "helpers/balancingtables.html", { "tables": balancingTables })

@csrf_exempt
def getBalancingTableJson(request, tablename, limitFrom, limitTo, displayMode, logisticTime):
    for table in BalancingTableBase.__subclasses__():
        if tablename == table.__name__:
            balancingTable = table(int(limitFrom), int(limitTo), int(displayMode), int(logisticTime))
            return HttpResponse(balancingTable.GetJson(), content_type='application/json')

    raise Http404()

@csrf_exempt
def setBalancingTableValue(request):
    for table in BalancingTableBase.__subclasses__():
        if request.POST["tablename"] == table.__name__:
            balancingTable = table(0,0)
            balancingTable.SetValueReceived(int(request.POST["column"]), int(request.POST["objID"]), request.POST["value"])
            return HttpResponse('{"result": "OK"}', content_type='application/json')

    return HttpResponse("{'result': 'FAIL'}", content_type='application/json')

def commandsView(request):
    commands = []
    for command in CommandBase.__subclasses__():
        commands.append(command.__name__)
    return render(request, "helpers/commands.html", { "commands": commands })

@csrf_exempt
def runCommand(request, commandname, arguments):
    for command in CommandBase.__subclasses__():
        if command.__name__ == commandname:
            output = command().RunCommand(arguments)
            output = output.replace('\n', '<br/>')
            return HttpResponse('{"output": "%s"}' % output, content_type="application/json")

    return HttpResponse('{"output": "Error: command not found!"}', content_type="application/json")

def researchOverview(request):
    devProjects = []
    for devProj in DevelopmentProject.objects.all():
        devProjects.append({
            "id": devProj.id,
            "name": devProj.Name,
        })
    return render(request, "helpers/researchoverview.html", { "devProjects": devProjects })

def researchDetail(request, projectID):
    project = get_object_or_404(DevelopmentProject, pk=projectID)
    prerequisites = []
    leadsTo = []
    modules = []
    buildables = []
    productTypes = []

    allProjects = DevelopmentProject.objects.all()
    for proj in allProjects:
        required = project.RequiredProjects.all()
        if proj in required:
            prerequisites.append({
                "id": proj.id,
                "name": proj.Name,
            })
        required = proj.RequiredProjects.all()
        if project in required:
            leadsTo.append({
                "id": proj.id,
                "name": proj.Name
            })

    allModules = Module.objects.all()
    for m in allModules:
        if m in project.UnlocksModules.all():
            modules.append({
                "id": m.id,
                "name": m.Name,
            })

    allBuildables = ObjectType.objects.all()
    for b in allBuildables:
        if b in project.UnlocksBuildables.all():
            buildables.append({
                "id": b.id,
                "name": b.Name,
            })

    allProductTypes = ProductType.objects.all()
    for p in allProductTypes:
        if p in project.UnlocksProductTypes.all():
            productTypes.append({
                "id": p.id,
                "name": p.Name
            })

    detailInformation = {
        "project": {
            "name": project.Name,
            "id": project.id,
        },
        "prerequisites": prerequisites,
        "leadsTo": leadsTo,
        "modules": modules,
        "buildables": buildables,
        "productTypes": productTypes,
    }
    return render(request, "helpers/researchdetail.html", detailInformation)