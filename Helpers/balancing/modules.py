from balancingtablebase import *
from Production.models import *
from ObjectTypes.models import *
from Tuning.models import *

class ModuleStackSizeColumn(ColumnBase):
    def GetHeader(self):
        return "StackSize"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(module.Material.StackSize)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        module.Material.StackSize = int(value)
        module.Material.save()

class ModuleProductionTimeColumn(ColumnBase):
    def GetHeader(self):
        return "Production Time"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            craftingDuration = 0
            craftingDurationQuery = CrafterPropertyModuleDuration.objects.filter(Module=module)
            if craftingDurationQuery.exists():
                craftingDuration = craftingDurationQuery.all()[0].Duration
            rows.append(craftingDuration)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        craftingDurationQuery = CrafterPropertyModuleDuration.objects.filter(Module=module)
        if craftingDurationQuery.exists():
            property = craftingDurationQuery.all()[0]
            property.Duration = int(value)
            property.save()

class ModuleRawMaterialCostColumn(ColumnBase):
    def GetHeader(self):
        return "Raw Material Cost"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append("%.2f" % module.rawMaterialCost())
        return rows

class NumModulesPerDay(ColumnBase):
    def GetHeader(self):
        return "max Modules per day"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        rows = []
        for module in query.all():
            rows.append("%.2f" % (secondsPerDay / getModuleTotalProductionTime(module)))
        return rows

def getModuleTotalProductionTime(module):
    totalTime = 0
    for inputMat in module.InputMaterials.all():
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            totalTime += getModuleTotalProductionTime(moduleMatQuery.all()[0]) * inputMat.Amount
    craftingDuration = CrafterPropertyModuleDuration.objects.filter(Module=module)
    if craftingDuration.exists():
        totalTime += craftingDuration.all()[0].Duration
    return totalTime

class ModuleTotalProductionTimeColumn(ColumnBase):
    def GetHeader(self):
        return "Total production time"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(getModuleTotalProductionTime(module))
        return rows

def getModuleNumProductionSteps(module):
    steps = 1
    for inputMat in module.InputMaterials.all():
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            steps += getModuleNumProductionSteps(moduleMatQuery.all()[0]) * inputMat.Amount
    return steps

class ModuleNumProductionSteps(ColumnBase):
    def GetHeader(self):
        return "Num Steps"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(getModuleNumProductionSteps(module))
        return rows

class ModuleSellPriceColumn(ColumnBase):
    def GetHeader(self):
        return "Sell Price"

    def GetRowStrings(self, query):
        addCostPerStep = float(TuningValue.objects.get(Name="ModuleSellPriceAddCostPerStep").Value)
        materialCostFactor = float(TuningValue.objects.get(Name="ModuleSellPriceMaterialCostFactor").Value)
        rows = []
        for module in query.all():
            price = getModuleNumProductionSteps(module) * addCostPerStep
            price += module.rawMaterialCost() * materialCostFactor
            rows.append(price)
        return rows

class ModuleProfitPerDay(ColumnBase):
    def GetHeader(self):
        return "Profit per day"

    def GetRowStrings(self, query):
        addCostPerStep = float(TuningValue.objects.get(Name="ModuleSellPriceAddCostPerStep").Value)
        materialCostFactor = float(TuningValue.objects.get(Name="ModuleSellPriceMaterialCostFactor").Value)
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for module in query.all():
            rawMaterialCost = module.rawMaterialCost()
            productionTime = getModuleTotalProductionTime(module)
            sellPrice = getModuleNumProductionSteps(module) * addCostPerStep
            sellPrice += rawMaterialCost * materialCostFactor
            productionCost = rawMaterialCost + employeeWagePerSecond * productionTime
            profitPerModule = sellPrice - productionCost

            rows.append("%.2f" % (secondsPerDay * (profitPerModule / productionTime)))
        return rows

class ModuleBalancingTable(BalancingTableBase):
    BalancingTableIdentifier = "Modules"
    def __init__(self, limitFrom, limitTo):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleProductionTimeColumn())
        self.AddColumn(ModuleNumProductionSteps())
        self.AddColumn(ModuleTotalProductionTimeColumn())
        self.AddColumn(NumModulesPerDay())
        self.AddColumn(ModuleRawMaterialCostColumn())
        self.AddColumn(ModuleSellPriceColumn())
        self.AddColumn(ModuleProfitPerDay())
