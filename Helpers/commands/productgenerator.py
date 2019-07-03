from Helpers.balancing.modules import *
from Tuning.models import TuningValue
from commandbase import CommandBase
from Production.models import *
from BalancingHelper.models import *
from ObjectTypes.models import *
from Research.models import *


# Generate All
class GenerateAllProducts(CommandBase):
    def RunCommand(self, commandline):
        string = ""
        for function in ProductFunction.objects.all():
            print("Generate for Function: " + function.Name)
            SampleProduct.objects.all().filter(ProductFunction=function, AutoGenerated="True").delete()
            for productType in function.ViableProductTypes.all():
                print("Generate for ProductType: " + productType.Name)
                string += generateProductByType(productType, function)+"<br><br>"
        return string

# Generate by Form Factor
class GenerateProductByType(CommandBase):
    def RunCommand(self, commandline):
        string = ""
        if ProductType.objects.all().filter(Name=commandline):
            productType = ProductType.objects.all().filter(Name=commandline)[0]
            print("Generate for ProductType: " + productType.Name)
            SampleProduct.objects.all().filter(ProductType=productType, AutoGenerated="True").delete()
            for function in ProductFunction.objects.all().filter(ViableProductTypes=productType):
                print("Generate for Function: " + function.Name)
                string += generateProductByType(productType, function)+"<br><br>"
        else:
            return "Product Type Not Found"
        return string

# Generate by Function
class GenerateProductByFunction(CommandBase):
    def RunCommand(self, commandline):
        string = ""
        if ProductFunction.objects.all().filter(Name=commandline):
            function = ProductFunction.objects.all().filter(Name=commandline)[0]
            print("Generate for Function: " + function.Name)
            SampleProduct.objects.all().filter(ProductFunction=function, AutoGenerated="True").delete()
            for productType in function.ViableProductTypes.all():
                print("Generate for ProductType: " + productType.Name)
                string += generateProductByType(productType, function)+"<br><br>"
        else:
            return "Function Not Found"
        return string

# Call to generate a set of sample products for given function & form factor
def generateProductByType(productType, function):

    requirementList = []
    for requirement in function.FeatureRequirements.all():
        requirementList.append(requirement)

    moduleLists = {}
    moduleListsDesc = {}
    for slot in productType.Slots.all():
        list = []
        for module in Module.objects.all().filter(FitsIntoSlot=slot):
            list.append(module)
        list.sort(key=sortPrice)
        moduleLists[slot] = list

    mvpData = generateMVP(moduleLists.copy(), requirementList)
    if mvpData is not None:

        addProductToDB(function, productType, mvpData, "MVP")
        print("MVP | Success")

        optionalFeatures = function.getOptionalsDict(True)
        requiredFeatures = function.getRequirementDict(True)
        combinedFeatures = requiredFeatures.copy()
        combinedFeatures.update(optionalFeatures)
        drawbacks = function.getDrawbacksDict(True)

        drawbackData = checkForBestFeatures(moduleLists.copy(), mvpData.copy(), requirementList, drawbacks.copy(), False)
        if drawbackData is not None:
            addProductToDB(function, productType, drawbackData, "MVP+")
            print("MVP+ | Success")

        requirementData = checkForBestFeatures(moduleLists.copy(), mvpData.copy(), requirementList, requiredFeatures)
        if requirementData is not None:
            addProductToDB(function, productType, requirementData, "Requirements")
            print("Requirements | Success")

            bestRequirementData = checkForBestFeatures(moduleLists.copy(), requirementData.copy(), requirementList, drawbacks, False)
            if bestRequirementData is not None:
                addProductToDB(function, productType, bestRequirementData, "Requirements+")
                print("Requirements+ | Success")

        optionalData = checkForBestFeatures(moduleLists.copy(), mvpData.copy(), requirementList, optionalFeatures)
        if optionalData is not None:
            addProductToDB(function, productType, optionalData, "Optionals")
            print("Optional | Success")

            bestOptionalData = checkForBestFeatures(moduleLists.copy(), optionalData.copy(), requirementList, drawbacks, False)
            if bestOptionalData is not None:
                addProductToDB(function, productType, bestOptionalData, "Optional+")
                print("Optional+ | Success")

        combinedData = checkForBestFeatures(moduleLists.copy(), mvpData.copy(), requirementList, combinedFeatures)
        if combinedData is not None:
            addProductToDB(function, productType, combinedData, "Combined")
            print("Combined | Success")

            bestCombinedData = checkForBestFeatures(moduleLists.copy(), combinedData.copy(), requirementList, drawbacks, False)
            if bestCombinedData is not None:
                addProductToDB(function, productType, bestCombinedData, "Combined+")
                print("Combined+ | Success")

    else:
        print("MVP | Failed")
    return "done"


def generateMVP(moduleLists, requirements):
    activeModules = {}
    for slot in moduleLists:
        activeModules[slot] = None
    usedRessources = {}
    features = {}

    change = True
    while not isValidProduct(requirements, usedRessources, features) and change:
        change = False
        for slot, moduleList in moduleLists.items():
            if len(moduleList) > 0:
                if not slot.IsOptional and activeModules[slot] is None:
                    activeModules[slot] = updateValues(activeModules[slot], moduleList[0], usedRessources, features)
                    change = True
                else:
                    moduleIndex = checkModuleByRequirements(activeModules[slot], moduleList, requirements)
                    if moduleIndex > -1:
                        activeModules[slot] = updateValues(activeModules[slot], moduleList[moduleIndex], usedRessources, features)
                        change = True
                    else:
                        moduleIndex = checkModuleByFeatures(activeModules[slot], moduleList, requirements, usedRessources)
                        if moduleIndex > -1:
                            activeModules[slot] = updateValues(activeModules[slot], moduleList[moduleIndex], usedRessources, features)
                            change = True

    if isValidProduct(requirements, usedRessources, features):
        return activeModules
    else:
        return None

def checkForBestFeatures(moduleLists, activeModules, requirements, targetFeatures, searchBest = True):
    usedRessources = {}
    features = {}
    for module in activeModules.values():
        addModuleValues(module, usedRessources, features)
    currentIndex = {}
    for slot in moduleLists:
        currentIndex[slot] = -1
    testedSomething = True
    actualChange = False
    while testedSomething and targetFeatures is not None:
        testedSomething = False
        for slot, moduleList in moduleLists.items():
            index = checkModuleByFeatures(activeModules[slot], moduleLists[slot], requirements, targetFeatures, searchBest, usedRessources)
            if index > currentIndex[slot]:
                currentIndex[slot] = index
                if UpdateData(slot, moduleList[index], moduleLists, activeModules, usedRessources, features, requirements):
                    actualChange = True
                testedSomething = True
    if actualChange:
        return activeModules
    else:
        return None

def UpdateData(moduleSlot, module, moduleLists, activeModules, usedRessources, features, requirements):
    oldModules = {}
    oldModules[moduleSlot] = activeModules[moduleSlot]
    activeModules[moduleSlot] = updateValues(activeModules[moduleSlot], module, usedRessources, features)

    for slot, moduleList in moduleLists.items():
        if slot != moduleSlot:
            moduleIndex = checkModuleByFeatures(activeModules[slot], moduleList, requirements, usedRessources)
            if moduleIndex >= 0:
                oldModules[slot] = activeModules[slot]
                activeModules[slot] = updateValues(activeModules[slot], moduleList[moduleIndex], usedRessources, features)
    if isValidProduct(requirements, usedRessources, features):
        return True
    else:
        for slot in moduleLists:
            if slot in oldModules:
                removeModuleValue(activeModules[slot], usedRessources, features)
                addModuleValues(oldModules[slot], usedRessources, features)
                activeModules[slot] = updateValues(activeModules[slot], oldModules[slot], usedRessources, features)
        return False


def addProductToDB(function, productType, moduleData, nameIdentifier):
    sampleProduct = SampleProduct.objects.create(Name=function.Name+"_"+productType.Name+"_"+nameIdentifier, AutoGenerated=True, ProductFunction=function, ProductType=productType)
    moduleIDs = []
    for module in moduleData.values():
        if module is not None:
            moduleIDs.append(module.id)
    sampleProduct.Modules = moduleIDs
    sampleProduct.save()
    return True


# returns the amount of fulfilled requirements
def moduleRequirementAmount(module, requirements):
    count = 0
    if module is not None:
        for req in requirements:
            for feature in module.Features.all():
                if feature.ProductFeature == req.Feature and req.FeatureValue <= feature.FeatureValue:
                    count += 1
    return count

# checks if there is a module in list which fulfills more requirements than the previous one
# returns index of the module that fits
def checkModuleByRequirements(activeModule, moduleList, requirements):
    index = 0
    maxCount = 0 if activeModule is None else moduleRequirementAmount(activeModule, requirements)
    for mod in moduleList:
        if maxCount < moduleRequirementAmount(mod, requirements):
            return index
        index += 1
    return -1

# checks and returns the sum of features values in a module of given features (capped)
def moduleFeatureAmount(module, features):
    count = 0
    if module is not None:
        for feature in module.Features.all():
            if feature.ProductFeature.Name in features:
                count += feature.FeatureValue if feature.FeatureValue <= features[feature.ProductFeature.Name] else features[feature.ProductFeature.Name]
    return count

# checking if and which module from a list fulfills more features from the feature list (capped)
# returns module index of module that has the highest feature amount while having same amount or more requirements that it fulfills
def checkModuleByFeatures(activeModule, moduleList, requirements, features, searchBest = True, lockedFeatures = None):
    index = 0
    savedIndex = -1
    requirementCount = moduleRequirementAmount(activeModule, requirements)
    bestValue = 0 if activeModule is None else moduleFeatureAmount(activeModule, features)
    lockedValue = 0
    lockedOriginalValue = 0
    if lockedFeatures is not None:
        lockedOriginalValue = moduleFeatureAmount(activeModule, lockedFeatures)


    for module in moduleList:
        featureAmount = moduleFeatureAmount(module, features)
        if lockedFeatures is not None:
            lockedValue = moduleFeatureAmount(module, lockedFeatures)
        if requirementCount <= moduleRequirementAmount(module, requirements) and lockedValue >= lockedOriginalValue:
            if searchBest and bestValue < featureAmount:
                bestValue = featureAmount
                savedIndex = index
            elif not searchBest and bestValue > featureAmount:
                bestValue = featureAmount
                savedIndex = index
        index += 1
    return savedIndex

def updateValues(oldModule, newModule, usedRessources, features):
    removeModuleValue(oldModule, usedRessources, features)
    addModuleValues(newModule, usedRessources, features)
    return newModule


def removeModuleValue(oldMod, usedRessources, features):
    if oldMod is not None:
        for feature in oldMod.Features.all():
            features[feature.ProductFeature.Name] -= feature.FeatureValue
            if len(feature.ProductFeature.MainFeature.all()) > 0:
                usedRessources[feature.ProductFeature.MainFeature.all()[0].Name] -= feature.FeatureValue

def addModuleValues(newMod, usedRessources, features):
    if newMod is not None:
        for feature in newMod.Features.all():
            if feature.ProductFeature.Name in features:
                features[feature.ProductFeature.Name] += feature.FeatureValue
            else:
                features[feature.ProductFeature.Name] = feature.FeatureValue
            if len(feature.ProductFeature.MainFeature.all()) > 0:
                if feature.ProductFeature.MainFeature.all()[0].Name in usedRessources:
                    usedRessources[feature.ProductFeature.MainFeature.all()[0].Name] += feature.FeatureValue
                else:
                    usedRessources[feature.ProductFeature.MainFeature.all()[0].Name] = feature.FeatureValue

def sortPrice(module):
    return module.BaseMarketPrice

def isValidProduct(requirements, usedRessources, features):
    for req in requirements:
        if req.Feature.Name not in features:
            return False
        else:
            if req.FeatureValue > features[req.Feature.Name]:
                return False

    for key, value in usedRessources.items():
        if value <= 0:
            return True
        if key not in features:
            return False
        else:
            if value > features[key]:
                return False
    return True