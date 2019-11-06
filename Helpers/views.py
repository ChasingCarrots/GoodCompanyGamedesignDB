# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from helpers import *
from balancing.modules import *
# from balancing.products import *
from commands.sanitychecks import *
from commands.tempcommands import *


def productbuilder(request):
    productTypes = []
    for productType in ProductType.objects.all().order_by("Name"):

        fields = []
        for field in productType.GridFields.all():
            fields.append({
                "x": field.x,
                "y": field.y
            })

        phases = []
        for phase in productType.MarketPhases.all().order_by("PhaseIndex"):

            pos = []
            for feature in phase.PositiveFeatures.all():
                pos.append({
                    "feature": feature.Feature,
                    "value": feature.Max
                })

            neg = []
            for feature in phase.NegativeFeatures.all():
                neg.append({
                    "feature": feature.Feature,
                    "value": feature.Min
                })

            phases.append({
                "name": phase.Name,
                "index": phase.PhaseIndex,
                "positiveFeatures": pos,
                "negativeFeatures": neg
            })

        cases = []
        for case in productType.Cases.all():

            bfields = []
            for field in case.BlockingGridFields.all():
                bfields.append({
                    "x": field.X,
                    "y": field.Y
                })

            cases.append({
                "moduleid": case.CaseModule.id,
                "fields": bfields
            })

        productTypes.append({
            "id": productType.id,
            "name": productType.Name,
            "icon": productType.IconAssetID,
            "phases": phases,
            "cases": cases,
            "fields": fields
        })

    moduleList = []
    for module in Module.objects.all().order_by("Name"):
        hasFields = False
        if module.GridFields.all():
            hasFields = True

        fields = []
        fcount = 0
        for field in module.GridFields.all():
            fcount = fcount + 1
            fields.append({
                "x": field.x,
                "y": field.y
            })

        features = []
        for feature in module.Features.all():
            features.append({
                "feature": feature.ProductFeature,
                "value": feature.FeatureValue
            })

        moduleList.append({
            "id": module.id,
            "name": module.Name,
            "icon": module.IconAssetID,
            "fields": fields,
            "fieldcount": fcount,
            "features": features,
            "price": module.BaseMarketPrice,
            "hasFields": hasFields
        })

    featureList = []
    for feature in ProductFeature.objects.all().order_by("Name"):
        featureList.append({
            "id": feature.id,
            "name": feature.Name,
            "symbol": feature.HelperEmoji
        })

    return render(request, "helpers/productbuilder.html", {
        "productTypes": productTypes,
        "moduleList": moduleList,
        "featureList": featureList,
    })


def productTypeOverview(request):
    productTypes = []

    commands = []
    for command in CommandBase.__subclasses__():
        commands.append(command.__name__)

    for productType in ProductType.objects.all().order_by("Name"):


        productTypes.append({
            "id": productType.id,
            "name": productType.Name,
            "value": productType.BaseMarketPrice,
            "icon": productType.IconAssetID
        })

    return render(request, "helpers/producttypeoverview.html", {
        "productTypes": productTypes,
    })


def productTypeDetail(request, typeID):
    productType = get_object_or_404(ProductType, pk=typeID)
    productSlots = []
    modules = []

    moduleCount = 0
    functionCount = 0

    return render(request, "helpers/producttypedetail.html", {
        "productType": {
            "id": productType.id,
            "name": productType.Name,
            "icon": productType.IconAssetID,
            "functionCound": functionCount,
            "moduleCount": moduleCount
        }
    })


def moduleCategoryOverview(request):
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

    return render(request, "helpers/modulecategories.html", {"categories": categories})


def modulePathDetails(request, pathID):
    path = get_object_or_404(CriticalModulePath, pk=pathID)

    modules = []
    _baseHandlingtime = 3.0
    _handlingtimePerMaterial = 0.5
    for module in path.Modules.all().order_by("PathPosition"):
        employeeCostSlow = employeeCostPerSecond() * getComponentCraftingTime(module.Module, _baseHandlingtime,
                                                                              _handlingtimePerMaterial, True, False,
                                                                              True) / module.Module.OutputAmount
        employeeCostFast = employeeCostPerSecond() * getComponentCraftingTime(module.Module, _baseHandlingtime,
                                                                              _handlingtimePerMaterial, True, True,
                                                                              True) / module.Module.OutputAmount
        totalSlow = (employeeCostSlow + module.Module.rawMaterialCost())
        totalQuick = (employeeCostFast + module.Module.rawMaterialCost())
        modules.append({
            "Module": module.Module,
            "id": module.id,
            "position": module.PathPosition,
            "expectedPosition": module.getExpectedPathPosition(),
            "progression": module.getProgressionPoint(),
            "initialCosts": module.getExpectedInitialCosts(),
            "minimumCosts": module.getExpectedMinimumCosts(),
            "sellPrice": module.getExpectedSellPrice(),
            "actualMaxCost": totalSlow,
            "actualMinCost": totalQuick,
            "actualSellPrice": module.Module.BaseMarketPrice,
        })

    positionData = []
    for i in range(0, 11):
        positionData.append({
            "position": i,
            "progression": path.getProgressionPoint(i),
            "initialCosts": path.getExpectedInitialCosts(i),
            "minimumCosts": path.getExpectedMinimumCosts(i),
            "sellPrice": path.getExpectedSellPrice(i),
        })

    if len(path.NegativeFeatures.all()) > 0:
        negValue = path.NegativeFeatureValue / len(path.NegativeFeatures.all())
    else:
        negValue = 0

    if len(path.PositiveFeatures.all()) > 0:
        posValue = path.PositiveFeatureValue / len(path.PositiveFeatures.all())
    else:
        posValue = 0

    return render(request, "helpers/modulepathdetails.html", {
        "path": path,
        "moduleCount": len(path.Modules.all()),
        "posValue": posValue,
        "negValue": negValue,
        "posFeatures": path.PositiveFeatures.all(),
        "negFeatures": path.NegativeFeatures.all(),
        "modules": modules,
        "positionData": positionData,
    })


def moduleOverview(request):
    modules = []
    for module in Module.objects.all().order_by("BaseMarketPrice"):
        modules.append({
            "id": module.id,
            "icon": module.IconAssetID,
            "name": module.Name,
            "matCost": module.rawMaterialCost(),
            "income": module.BaseMarketPrice
        })
    return render(request, "helpers/moduleoverview.html", {"modules": modules})


def moduleDetail(request, moduleID):
    module = get_object_or_404(Module, pk=moduleID)

    featureValue = 0.0
    drawbackValue = 0.0
    moduleSize = 0.0

    for feature in module.Features.all():
        if feature.ProductFeature.IsDrawback:
            drawbackValue = drawbackValue + feature.FeatureValue
        else:
            featureValue = featureValue + feature.FeatureValue

    for field in module.GridFields.all():
        moduleSize = moduleSize + 1

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
            "totalcost": cost * moduleInputMat.Amount / float(module.OutputAmount),
        })

    usedInModules = []
    usedInModCount = 0
    for mod in Module.objects.all():
        if mod.InputMaterials.all().filter(Material=module.Material).exists():
            usedInModules.append(mod)
            usedInModCount += 1

    features = []
    for feature in module.Features.all():
        features.append(feature)

    tableList = []
    _baseHandlingtime = 3.0
    _handlingtimePerMaterial = 0.5
    handlingCost = employeeCostPerSecond() * (
                len(module.InputMaterials.all()) * _handlingtimePerMaterial + _baseHandlingtime) / module.OutputAmount
    employeeCostSlow = employeeCostPerSecond() * getComponentCraftingTime(module, _baseHandlingtime,
                                                                          _handlingtimePerMaterial, True, False, False)
    employeeCostFast = employeeCostPerSecond() * getComponentCraftingTime(module, _baseHandlingtime,
                                                                          _handlingtimePerMaterial, True, True, False)

    for object in ObjectType.objects.filter(CrafterProperty__isnull=False).order_by("Name"):
        for possibleModule in object.CrafterProperty.PossibleModules.all():
            if possibleModule.Module == module:
                productionCost = employeeCostPerSecond() * possibleModule.Duration / module.OutputAmount
                totalSlow = (productionCost + handlingCost + employeeCostSlow + module.rawMaterialCost())
                totalQuick = (productionCost + handlingCost + employeeCostFast + module.rawMaterialCost())
                tableList.append({
                    "id": object.id,
                    "name": object.Name,
                    "productionTime": possibleModule.Duration / module.OutputAmount,
                    "productionCost": productionCost,
                    "productionRateSlow": 100 * productionCost / totalSlow,
                    "productionRateQuick": 100 * productionCost / totalQuick,
                    "handlingRateSlow": 100 * handlingCost / totalSlow,
                    "handlingRateQuick": 100 * handlingCost / totalQuick,
                    "preStepRateSlow": 100 * employeeCostSlow / totalSlow,
                    "preStepRateQuick": 100 * employeeCostFast / totalQuick,
                    "materialRateSlow": 100 * module.rawMaterialCost() / totalSlow,
                    "materialRateQuick": 100 * module.rawMaterialCost() / totalQuick,
                    "totalCostSlow": totalSlow,
                    "totalCostQuick": totalQuick,
                })

    criticalModule = ModulePathObject.objects.all().filter(Module=module)
    criticalPath = {}
    if criticalModule:
        criticalPath["position"] = criticalModule[0].PathPosition
        criticalPath["expectedPosition"] = criticalModule[0].getExpectedPathPosition()
        criticalPath["id"] = criticalModule[0].Path.id
        criticalPath["name"] = criticalModule[0].Path.Name
        criticalPath["progression"] = criticalModule[0].getProgressionPoint()
        criticalPath["mainFeature"] = criticalModule[0].Path.MainFeature
        criticalPath["positiveFeatures"] = criticalModule[0].Path.PositiveFeatures.all()
        criticalPath["negativeFeatures"] = criticalModule[0].Path.NegativeFeatures.all()
        criticalPath["initialCosts"] = criticalModule[0].getExpectedInitialCosts()
        criticalPath["minimumCosts"] = criticalModule[0].getExpectedMinimumCosts()
        criticalPath["sellPrice"] = criticalModule[0].getExpectedSellPrice()

    totalTime = getComponentCraftingTime(module, 0, 0, False, False) + module.AssemblyTime
    featureRating = 0.0
    if module.rawMaterialCost() > 0:
        featureRating = (featureValue/module.rawMaterialCost())*5.0
    drawbackRating = 0.0
    if drawbackValue > 0:
        drawbackRating = (float(featureValue)/float(drawbackValue))
    sizeRating = 0.0
    if moduleSize > 0:
        sizeRating = (featureValue/moduleSize)*3.0
    timeRating = 0.0
    if totalTime > 0:
        timeRating = (featureValue/totalTime)*1.0
    totalRating = (featureRating + featureRating + drawbackRating + sizeRating + timeRating) * 0.2

    return render(request, "helpers/moduledetail.html", {
        "module": {
            "name": module.Name,
            "inputMaterials": moduleInputMaterials,
            "features": features,
            "icon": module.IconAssetID,
            "id": module.id,
            "materialId": module.Material.id,
            "complexity": getComponentComplexity(module),
            "costs": totalCostPerComponent(module, 0),
            "materialcosts": module.rawMaterialCost(),
            "profit": totalProfitPerComponent(module, 0),
            "income": module.BaseMarketPrice,
            "profitability": getComponentProfitability(module, 0),
            "craftingTime": getComponentCraftingTime(module, 0, 0, False, False),
            "perMinuteRate": componentsPerSecond(module, 0) * 60,
            "perMinuteProfit": componentProfitPerSecond(module, 0) * 60,
            "outputAmount": module.OutputAmount,
            "usedinmodulescount": usedInModCount,
            "handlingCost": handlingCost,
            "employeeCostSlow": employeeCostSlow,
            "employeeCostQuick": employeeCostFast,
        },
        "balancing": {
            "totalRating": totalRating,
            "featureRating": featureRating,
            "drawbackRating": drawbackRating,
            "sizeRating": sizeRating,
            "timeRating": timeRating,
            "featureCount": featureValue,
            "materialCosts": module.rawMaterialCost(),
            "drawbackCount": drawbackValue,
            "moduleSize": moduleSize,
            "totalTime": totalTime,
        },
        "tableList": tableList,
        "criticalPath": criticalPath,
        "materials": moduleBaseMaterials,
        "usedinmodules": usedInModules,
        "total": {
            "amount": totalAmount,
            "totalcost": totalCost,
        },
        "commands": commands,
    })


def materialOverview(request):
    materials = []
    # get all materials
    for material in Material.objects.filter(module=None).all().order_by("StackBuyPrice"):
        materials.append({
            "id": material.id,
            "name": material.Name,
            "cost": material.getPricePerUnit(),
            "icon": material.IconAssetID
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

    productTypes = {}
    for productType in ProductType.objects.all():
        productTypes[str(productType.id)] = productType.getJsonObject()

    productFeatures = {}
    for productFeature in ProductFeature.objects.all():
        productFeatures[str(productFeature.id)] = productFeature.getJsonObject()

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

    buildableCategories = {}
    for category in BuildabelCategory.objects.all():
        buildableCategories[str(category.id)] = category.getJsonObject()

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

    moduleCategories = {}
    for modCat in ModuleCategory.objects.all():
        moduleCategories[str(modCat.id)] = modCat.getJsonObject()

    return HttpResponse(json.dumps({
        "Materials": materials,
        "Modules": modules,
        "ProductTypes": productTypes,
        "ProductFeatures": productFeatures,
        "ObjectTypes": objectTypes,
        "MovableProperties": movableProperties,
        "ObjectLookProperties": objectLookProperties,
        "IconProperties": iconProperties,
        "InventoryProperties": inventoryProperties,
        "StorageProperties": storageProperties,
        "BuildableCategories": buildableCategories,
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
        "DevelopmentProjects": developmentProjects,
        "ModuleCategories": moduleCategories
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
    return render(request, "helpers/balancingtables.html", {"tables": balancingTables})


@csrf_exempt
def getBalancingTableJson(request, tablename, limitFrom, limitTo, displayMode, logisticTime, option):
    for table in BalancingTableBase.__subclasses__():
        if tablename == table.__name__:
            balancingTable = table(int(limitFrom), int(limitTo), int(displayMode), int(logisticTime), option)
            return HttpResponse(balancingTable.GetJson(), content_type='application/json')

    raise Http404()


@csrf_exempt
def setBalancingTableValue(request):
    for table in BalancingTableBase.__subclasses__():
        if request.POST["tablename"] == table.__name__:
            balancingTable = table(0, 0)
            balancingTable.SetValueReceived(int(request.POST["column"]), int(request.POST["objID"]),
                                            request.POST["value"])
            return HttpResponse('{"result": "OK"}', content_type='application/json')

    return HttpResponse("{'result': 'FAIL'}", content_type='application/json')


def commandsView(request):
    commands = []
    for command in CommandBase.__subclasses__():
        commands.append(command.__name__)
    return render(request, "helpers/commands.html", {"commands": commands})


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
        modules = []
        buildables = []
        productTypes = []
        functions = []
        data = []
        projectNetworth = 0
        projects = []

        for p in devProj.RequiredForProjects.all():
            projects.append({
                "id": p.id,
                "name": p.Name,
                "icon": p.IconAssetID,
            })

        for m in devProj.UnlocksModules.all():
            modules.append({
                "id": m.id,
                "name": m.Name,
                "icon": m.IconAssetID,
            })

        for b in devProj.UnlocksBuildables.all():
            icon = ""
            for i in IconProperty.objects.all().filter(ObjectType=b):
                icon = b.IconProperty.IconAssetID
            buildables.append({
                "id": b.id,
                "name": b.Name,
                "icon": icon,
            })

        for p in devProj.UnlocksProductTypes.all():
            productTypes.append({
                "id": p.id,
                "name": p.Name,
                "icon": p.IconAssetID
            })

        for requiredData in devProj.RequiredData.all():
            data.append({
                "id": requiredData.DataType.id,
                "name": requiredData.DataType.Name,
                "icon": requiredData.DataType.IconAssetID,
                "amount": requiredData.Amount,
                "value": requiredData.DataType.NetWorth,
                "networth": requiredData.Amount * requiredData.DataType.NetWorth,
            })
            projectNetworth += requiredData.Amount * requiredData.DataType.NetWorth

        devProjects.append({
            "id": devProj.id,
            "hidden": devProj.IsHidden,
            "name": devProj.Name,
            "icon": devProj.IconAssetID,
            "networth": projectNetworth,
            "modules": modules,
            "buildables": buildables,
            "productTypes": productTypes,
            "data": data,
            "projects": projects,
        })
    return render(request, "helpers/researchoverview.html", {"devProjects": devProjects})


def researchDetail(request, projectID):
    project = get_object_or_404(DevelopmentProject, pk=projectID)
    prerequisites = []
    leadsTo = []
    modules = []
    buildables = []
    productTypes = []
    data = []
    projectNetworth = 0

    allProjects = DevelopmentProject.objects.all()
    for proj in allProjects:
        required = project.RequiredProjects.all()
        if proj in required:
            prerequisites.append({
                "id": proj.id,
                "name": proj.Name,
                "icon": proj.IconAssetID,
            })
        required = proj.RequiredProjects.all()
        if project in required:
            leadsTo.append({
                "id": proj.id,
                "name": proj.Name,
                "icon": proj.IconAssetID,
            })

    allModules = Module.objects.all()
    for m in allModules:
        if m in project.UnlocksModules.all():
            modules.append({
                "id": m.id,
                "name": m.Name,
                "icon": m.IconAssetID,
            })

    allBuildables = ObjectType.objects.all()
    for b in allBuildables:
        if b in project.UnlocksBuildables.all():
            icon = ""
            for i in IconProperty.objects.all().filter(ObjectType=b):
                icon = b.IconProperty.IconAssetID
            buildables.append({
                "id": b.id,
                "name": b.Name,
                "icon": icon,
            })

    allProductTypes = ProductType.objects.all()
    for p in allProductTypes:
        if p in project.UnlocksProductTypes.all():
            productTypes.append({
                "id": p.id,
                "name": p.Name,
                "icon": p.IconAssetID
            })

    for requiredData in project.RequiredData.all():
        data.append({
            "id": requiredData.DataType.id,
            "name": requiredData.DataType.Name,
            "icon": requiredData.DataType.IconAssetID,
            "amount": requiredData.Amount,
            "value": requiredData.DataType.NetWorth,
            "networth": requiredData.Amount * requiredData.DataType.NetWorth,
        })
        projectNetworth += requiredData.Amount * requiredData.DataType.NetWorth

    detailInformation = {
        "project": {
            "name": project.Name,
            "id": project.id,
            "icon": project.IconAssetID,
            "networth": projectNetworth,
            "hidden": project.IsHidden,
        },
        "prerequisites": prerequisites,
        "leadsTo": leadsTo,
        "modules": modules,
        "buildables": buildables,
        "productTypes": productTypes,
        "data": data,
        "datacount": len(data),
    }
    return render(request, "helpers/researchdetail.html", detailInformation)


def ObjectOverview(request):
    crafterList = []
    for object in ObjectType.objects.all().filter(BuildableProperty__isnull=True).filter(
            CrafterProperty__isnull=False).order_by("Name"):
        crafterList.append({
            "id": object.id,
            "name": object.Name,
            "modulecount": len(object.CrafterProperty.PossibleModules.all()),
        })

    inventoryList = []
    for object in ObjectType.objects.all().filter(BuildableProperty__isnull=True).filter(
            InventoryProperty__isnull=False).order_by("Name"):
        if "DECO_" not in object.Name:
            inventoryList.append({
                "id": object.id,
                "name": object.Name,
                "slotcount": object.InventoryProperty.NumberOfSlots,
            })

    decoList = []
    for object in ObjectType.objects.all().filter(BuildableProperty__isnull=True).order_by("Name"):
        if "DECO_" in object.Name:
            decoList.append({
                "id": object.id,
                "name": object.Name,
            })

    return render(request, "helpers/objectoverview.html", {
        "crafterList": crafterList,
        "inventoryList": inventoryList,
        "decoList": decoList,
    })


def ObjectDetails(request, objectID):
    object = get_object_or_404(ObjectType, pk=objectID)

    employeeCostsPerSecond = float(TuningValue.objects.all().filter(Name="EmployeeWage")[0].Value) / float(
        TuningValue.objects.all().filter(Name="SecondsPerDay")[0].Value)

    possibleModules = []
    try:
        crafter = object.CrafterProperty
    except:
        possibleModules = None
    else:
        for module in crafter.PossibleModules.all():
            possibleModules.append({
                "id": module.Module.id,
                "name": module.Module.Name,
                "duration": module.Duration,
                "icon": module.Module.IconAssetID,
                "materials": module.Module.InputMaterials.all(),
                "outputAmount": module.Module.OutputAmount,
                "materialCosts": module.Module.rawMaterialCost(),
                "employeeCosts": employeeCostsPerSecond * module.Duration / module.Module.OutputAmount,
            })

    return render(request, "helpers/objectdetailview.html", {
        "object": object,
        "employeeCostsPerSecond": employeeCostsPerSecond,
        "possibleModules": possibleModules,
    })


def viewAll(request, displaymode):
    url = "https://www.chasing-carrots.com/download/goodcompany/viewall.htm"

    materialList = []
    for material in Material.objects.all().filter(StackBuyPrice__gt=0):
        materialList.append({
            "id": material.id,
            "name": material.Name,
            "icon": material.IconAssetID,
            "price": material.StackBuyPrice,
            "stacksize": material.StackSize
        })

    slotList = []
    for slot in ModuleSlotType.objects.all():
        moduleList = []
        for module in slot.FittingModule.all():
            tables = []
            for crafterModule in CrafterPropertyModuleDuration.objects.all().filter(Module=module):
                tables.append({
                    "id": crafterModule.CrafterProperty.ObjectType.id,
                    "name": crafterModule.CrafterProperty.ObjectType.Name
                })

            researches = []
            for research in module.UnlockedByResearch.all():
                researches.append({
                    "id": research.id,
                    "name": research.Name
                })

            moduleList.append({
                "id": module.id,
                "name": module.Name,
                "icon": module.IconAssetID,
                "researches": researches,
                "tables": tables
            })

        typeList = []
        for type in slot.UsedInProductType.all():
            typeList.append({
                "id": type.id,
                "name": type.Name
            })

        slotList.append({
            "id": slot.id,
            "name": slot.Name,
            "modules": moduleList,
            "types": typeList
        })

    componentList = []
    for module in Module.objects.all():
        tables = []
        for crafterModule in CrafterPropertyModuleDuration.objects.all().filter(Module=module):
            tables.append({
                "id": crafterModule.CrafterProperty.ObjectType.id,
                "name": crafterModule.CrafterProperty.ObjectType.Name
            })

        researches = []
        for research in module.UnlockedByResearch.all():
            researches.append({
                "id": research.id,
                "name": research.Name
            })

        isActive = "/"
        if ModulePathObject.objects.all().filter(Module=module):
            isActive = "Active"

        componentList.append({
            "id": module.id,
            "name": module.Name,
            "icon": module.IconAssetID,
            "isActive": isActive,
            "researches": researches,
            "tables": tables
        })

    moduleList = []
    for module in Module.objects.all():
        tables = []
        for crafterModule in CrafterPropertyModuleDuration.objects.all().filter(Module=module):
            tables.append({
                "id": crafterModule.CrafterProperty.ObjectType.id,
                "name": crafterModule.CrafterProperty.ObjectType.Name
            })

        researches = []
        for research in module.UnlockedByResearch.all():
            researches.append({
                "id": research.id,
                "name": research.Name
            })

        isActive = "/"
        if ModulePathObject.objects.all().filter(Module=module):
            isActive = "Active"

        moduleList.append({
            "id": module.id,
            "name": module.Name,
            "icon": module.IconAssetID,
            "isActive": isActive,
            "researches": researches,
            "tables": tables
        })

    tableList = []
    for object in ObjectType.objects.all().filter(BuildableProperty__isnull=False).order_by("Name"):

        researches = []
        for research in object.UnlockedByResearch.all():
            researches.append({
                "id": research.id,
                "name": research.Name
            })

        print(object.BuildableProperty.BuildsObjectConnection)

        tableList.append({
            "id": object.id,
            "tableid": object.BuildableProperty.BuildsObjectConnection.BuildsObject.id,
            "name": object.BuildableProperty.BuildsObjectConnection.BuildsObject.Name,
            "researches": researches
        })

    productTypeList = []
    for type in ProductType.objects.all():

        researches = []
        for research in type.UnlockedByResearch.all():
            researches.append({
                "id": research.id,
                "name": research.Name
            })

        slots = []
        for slot in type.Slots.all():
            slots.append({
                "id": slot.id,
                "name": slot.Name
            })

        productTypeList.append({
            "id": type.id,
            "name": type.Name,
            "icon": type.IconAssetID,
            "slots": slots,
            "researches": researches
        })

    projectList = []
    for project in DevelopmentProject.objects.all():

        researches = []
        for research in project.RequiredForProjects.all():
            researches.append({
                "id": research.id,
                "name": research.Name
            })

        modules = []
        for module in project.UnlocksModules.all():
            modules.append({
                "id": module.id,
                "name": module.Name
            })

        buildables = []
        for buildable in project.UnlocksBuildables.all():
            buildables.append({
                "id": buildable.id,
                "name": buildable.Name
            })

        types = []
        for type in project.UnlocksProductTypes.all():
            types.append({
                "id": type.id,
                "name": type.Name
            })

        projectList.append({
            "id": project.id,
            "name": project.Name,
            "icon": project.IconAssetID,
            "researches": researches,
            "types": types,
            "buildables": buildables,
            "modules": modules,
        })

    htmlsite = "helpers/viewall.html"
    if displaymode == "csv":
        htmlsite = "helpers/viewallcsv.html"

    return render(request, htmlsite, {
        "url": url,
        "materialList": materialList,
        "componentList": componentList,
        "moduleList": moduleList,
        "slotList": slotList,
        "tableList": tableList,
        "productTypeList": productTypeList,
        "projectList": projectList
    })
