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

class ModuleOutputAmountColumn(ColumnBase):
    def GetHeader(self):
        return "Output Amount"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(module.OutputAmount)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        module.OutputAmount = int(value)
        module.save()

class ModuleProductionTimeColumn(ColumnBase):
    def GetHeader(self):
        return "Time/Stack"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            craftingDuration = 0
            craftingDurationQuery = CrafterPropertyModuleDuration.objects.filter(Module=module).order_by("id")
            if craftingDurationQuery.exists():
                craftingDuration = craftingDurationQuery.all()[0].Duration
            rows.append(craftingDuration)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        craftingDurationQuery = CrafterPropertyModuleDuration.objects.filter(Module=module).order_by("id")
        if craftingDurationQuery.exists():
            property = craftingDurationQuery.all()[0]
            property.Duration = int(value)
            property.save()

class ModuleRawMaterialCostColumn(ColumnBase):
    def GetHeader(self):
        return "Material Cost"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append("%.2f" % module.rawMaterialCost())
        return rows


class ModuleRawEmployeeCostColumn(ColumnBase):
    def GetHeader(self):
        return "Employee Cost"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeCostsPerDay = float(TuningValue.objects.get(Name="EmployeeWage").Value)
        rows = []
        for module in query.all():
            moduleProductionTime = getModuleTotalProductionTime(module)
            if moduleProductionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % ((moduleProductionTime / secondsPerDay) * employeeCostsPerDay))
        return rows

class ModuleCostColumn(ColumnBase):
    def GetHeader(self):
        return "Costs/Item"


    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for module in query.all():
            rawMaterialCost = module.rawMaterialCost()
            productionTime = getModuleTotalProductionTime(module)
            productionCost = rawMaterialCost + employeeWagePerSecond * productionTime

            if productionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (productionCost))
        return rows


class NumQueuesPerDay(ColumnBase):
    def GetHeader(self):
        return "Queues/Day"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        rows = []
        for module in query.all():
            moduleProductionTime = getModuleTotalProductionTime(module)
            if moduleProductionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (secondsPerDay / moduleProductionTime))
        return rows

class NumModulesPerDay(ColumnBase):
    def GetHeader(self):
        return "Modules/Day"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        rows = []
        for module in query.all():
            moduleProductionTime = getModuleProductionTime(module)
            if moduleProductionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (secondsPerDay / moduleProductionTime))
        return rows

def getModuleProductionTime(module):
    totalTime = 0
    craftingDuration = CrafterPropertyModuleDuration.objects.filter(Module=module).order_by("id")
    if craftingDuration.exists():
        totalTime += craftingDuration.all()[0].Duration / module.OutputAmount
    return totalTime

def getModuleTotalProductionTime(module):
    totalTime = 0
    for inputMat in module.InputMaterials.all():
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            totalTime += getModuleTotalProductionTime(moduleMatQuery.all()[0]) * inputMat.Amount
    craftingDuration = CrafterPropertyModuleDuration.objects.filter(Module=module).order_by("id")
    if craftingDuration.exists():
        totalTime += craftingDuration.all()[0].Duration / module.OutputAmount
    return totalTime

class ModuleTotalProductionTimeColumn(ColumnBase):
    def GetHeader(self):
        return "Queue Time"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(getModuleTotalProductionTime(module))
        return rows

def getModuleNumProductionSteps(module):
    steps = 1.0 / module.OutputAmount
    for inputMat in module.InputMaterials.all():
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            steps += getModuleNumProductionSteps(moduleMatQuery.all()[0]) * inputMat.Amount
    return steps

def getModuleNumMaterialSteps(module):
    steps = 0
    for inputMat in module.InputMaterials.all():
        steps += 1
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            steps += getModuleNumMaterialSteps(moduleMatQuery.all()[0])
    return steps

class ModuleNumProductionSteps(ColumnBase):
    def GetHeader(self):
        return "Steps"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append("%.2f"%getModuleNumProductionSteps(module))
        return rows

class ModuleBaseMarketPrice(ColumnBase):
    def GetHeader(self):
        return "BasePrice"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append("%.2f" % module.BaseMarketPrice)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        module.BaseMarketPrice = float(value)
        module.save()

class ModuleProfitPerDay(ColumnBase):
    def GetHeader(self):
        return "Profit per Day"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for module in query.all():
            rawMaterialCost = module.rawMaterialCost()
            productionTime = getModuleTotalProductionTime(module)
            sellPrice = module.BaseMarketPrice
            productionCost = rawMaterialCost + employeeWagePerSecond * productionTime
            profitPerModule = sellPrice - productionCost

            if productionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (secondsPerDay * (profitPerModule / productionTime)))
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay

        rawMaterialCost = module.rawMaterialCost()
        productionTime = getModuleTotalProductionTime(module)
        sellPrice = module.BaseMarketPrice
        productionCost = rawMaterialCost + employeeWagePerSecond * productionTime
        profitPerModule = sellPrice - productionCost

        module.BaseMarketPrice = float(value) / (secondsPerDay / productionTime) + productionCost
        module.save()

class ModuleProductionCostPerDay(ColumnBase):
    def GetHeader(self):
        return "Cost/Day"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for module in query.all():
            rawMaterialCost = module.rawMaterialCost()
            productionTime = getModuleTotalProductionTime(module)
            productionCost = rawMaterialCost + employeeWagePerSecond * productionTime

            if productionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (secondsPerDay * (productionCost / productionTime)))
        return rows

class ModuleProfitability(ColumnBase):
    def GetHeader(self):
        return "Profitability"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for module in query.all():
            rawMaterialCost = module.rawMaterialCost()
            productionTime = getModuleTotalProductionTime(module)
            sellPrice = module.BaseMarketPrice
            productionCost = rawMaterialCost + employeeWagePerSecond * productionTime

            if productionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (sellPrice/productionCost))
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay

        rawMaterialCost = module.rawMaterialCost()
        productionTime = getModuleTotalProductionTime(module)
        productionCost = rawMaterialCost + employeeWagePerSecond * productionTime

        module.BaseMarketPrice = float(value) * productionCost
        module.save()

class ModuleBalancingTable(BalancingTableBase):
    def __init__(self, limitFrom, limitTo):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleProductionTimeColumn())
        self.AddColumn(ModuleOutputAmountColumn())
        self.AddColumn(ModuleNumProductionSteps())
        #self.AddColumn(ModuleTotalProductionTimeColumn())
        self.AddColumn(NumModulesPerDay())
        #self.AddColumn(NumQueuesPerDay())
        #self.AddColumn(ModuleRawMaterialCostColumn())
        #self.AddColumn(ModuleRawEmployeeCostColumn())
        self.AddColumn(ModuleCostColumn())
        self.AddColumn(ModuleProductionCostPerDay())
        self.AddColumn(ModuleBaseMarketPrice())
        self.AddColumn(ModuleProfitability())
        self.AddColumn(ModuleProfitPerDay())
