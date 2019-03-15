from balancingtablebase import *
from Production.models import *
from ObjectTypes.models import *

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
            rows.append(module.rawMaterialCost())
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

class ModuleBalancingTable(BalancingTableBase):
    BalancingTableIdentifier = "modules"
    def __init__(self, limitFrom, limitTo):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleStackSizeColumn())
        self.AddColumn(ModuleProductionTimeColumn())
        self.AddColumn(ModuleTotalProductionTimeColumn())
        self.AddColumn(ModuleTotalProductionTimeColumn())
        self.AddColumn(ModuleTotalProductionTimeColumn())
        self.AddColumn(ModuleTotalProductionTimeColumn())
        self.AddColumn(ModuleTotalProductionTimeColumn())
