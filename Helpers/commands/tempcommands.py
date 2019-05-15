from Helpers.balancing.modules import getComponentProductionSteps
from Tuning.models import TuningValue
from commandbase import CommandBase
from Production.models import *
from ObjectTypes.models import *
from Research.models import *


class InitAllModuleMarketPrices(CommandBase):
    def RunCommand(self, commandline):
        if commandline != "iknow":
            return "THIS WILL OVERWRITE EVERY MODULE'S MARKETPRICE!\nAknowlege this fact by running with the commandline 'iknow'"

        numModules = 0
        addCostPerStep = float(TuningValue.objects.get(Name="ModuleSellPriceAddCostPerStep").Value)
        materialCostFactor = float(TuningValue.objects.get(Name="ModuleSellPriceMaterialCostFactor").Value)
        for module in Module.objects.all():
            price = getComponentProductionSteps(module, True) * addCostPerStep
            price += module.rawMaterialCost() * materialCostFactor
            module.BaseMarketPrice = price
            module.save()
            numModules += 1

        return "Changed the BaseMarketPrice of %d modules" % numModules