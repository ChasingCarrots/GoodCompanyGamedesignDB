from django.db.models import Count
from commandbase import CommandBase
from Production.models import *
from ObjectTypes.models import *
from Research.models import *

class CheckModuleDuplicateFeatures(CommandBase):
    def RunCommand(self, arguments):
        output = ""
        for module in Module.objects.all():
            modulesWithSameFeatures = set()
            setInitialized = False
            for feature in module.Features.all():
                otherModulesWithFeature = ModuleFeature.objects.exclude(id=feature.id)
                otherModulesWithFeature = otherModulesWithFeature.filter(ProductFeature=feature.ProductFeature, FeatureValue=feature.FeatureValue)
                otherModulesWithFeature = otherModulesWithFeature.annotate(num_features=Count("Module__Features"))
                otherModulesWithFeature = otherModulesWithFeature.filter(num_features=module.Features.count())
                if not otherModulesWithFeature.exists():
                    modulesWithSameFeatures.clear()
                    break

                otherModulesSet = set([moduleFeature.Module.id for moduleFeature in otherModulesWithFeature.all()])
                if not setInitialized:
                    modulesWithSameFeatures = otherModulesSet
                    setInitialized = True
                else:
                    modulesWithSameFeatures = modulesWithSameFeatures.intersection(otherModulesSet)
                if len(modulesWithSameFeatures) == 0:
                    break
            if len(modulesWithSameFeatures) != 0:
                output += "These modules have the same features: %s" % module.Name
                for otherModuleID in modulesWithSameFeatures:
                    output += ", %s" % Module.objects.get(id=otherModuleID).Name
                output +=".\n"
        if output == "":
            output = "No modules that have the same features were found."
        return output

def doModulesHaveSameRecipe(module1, module2):
    if module1.InputMaterials.count() != module2.InputMaterials.count():
        return False
    for input1 in module1.InputMaterials.all():
        if not module2.InputMaterials.filter(Material=input1.Material, Amount=input1.Amount):
            return False
    return True

class CheckModuleRecipeUniqueness(CommandBase):
    def RunCommand(self, arguments):
        output = ""
        checkedCombinations = {}
        for module1 in Module.objects.all():
            if not module1.id in checkedCombinations:
                checkedCombinations[module1.id] = [module1.id]
            for module2 in Module.objects.exclude(id__in=checkedCombinations[module1.id]):
                if doModulesHaveSameRecipe(module1, module2):
                    output += "%s and %s have the same recipe\n" % (module1.Name, module2.Name)
                checkedCombinations[module1.id].append(module2.id)
                if not module2.id in checkedCombinations:
                    checkedCombinations[module2.id] = [module2.id, module1.id]
                else:
                    checkedCombinations[module2.id].append(module1.id)
        if output == "":
            output = "No modules that have the same recipes were found."
        return output

class CheckModuleCraftability(CommandBase):
    def RunCommand(self, arguments):
        output = ""
        for module in Module.objects.all():
            if not CrafterPropertyModuleDuration.objects.filter(Module=module).exists():
                output += "%s (id: %d) can't be crafted on any crafter!\n" % (module, module.id)
        if output == "":
            output = "Every module can be crafted on at least one crafter!"
        return output

class ListNonResearchables(CommandBase):
    def RunCommand(self, arguments):
        output = ""
        for module in Module.objects.all():
            if not DevelopmentProject.objects.filter(UnlocksModules=module).exists():
                output += "Module %s (id:%d) has no research project.\n" % (module, module.id)
        for buildableProp in BuildableProperty.objects.all():
            buildableObjtype = buildableProp.ObjectType
            if not DevelopmentProject.objects.filter(UnlocksBuildables=buildableObjtype).exists():
                output += "Buildable %s (id:%d) has no research project.\n" % (buildableObjtype, buildableObjtype.id)
        for productType in ProductType.objects.all():
            if not DevelopmentProject.objects.filter(UnlocksProductTypes=productType).exists():
                output += "ProductType %s (id:%d) has no research project.\n" % (productType, productType.id)
        if output == "":
            output = "No Module or Buildable without research project found!"
        return output
