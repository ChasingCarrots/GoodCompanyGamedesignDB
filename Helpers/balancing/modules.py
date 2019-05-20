from balancingtablebase import *
from Production.models import *
from Research.models import *
from ObjectTypes.models import *
from Tuning.models import *

class ComponentBalancing(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentComplexity(displayMode, logisticTime))
        self.AddColumn(ComponentCosts(displayMode, logisticTime))
        self.AddColumn(ComponentSellPrice(displayMode, logisticTime))
        self.AddColumn(ComponentProfit(displayMode, logisticTime))
        self.AddColumn(ComponentProfitability(displayMode, logisticTime))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime))

class ComponentFinances(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentMaterialCosts(displayMode, logisticTime))
        self.AddColumn(ComponentEmployeeCosts(displayMode, logisticTime))
        self.AddColumn(ComponentSellPrice(displayMode, logisticTime))
        self.AddColumn(ComponentProfit(displayMode, logisticTime))
        self.AddColumn(ComponentProfitability(displayMode, logisticTime))
        self.AddColumn(ComponentsPerMinute(displayMode, logisticTime))
        self.AddColumn(ComponentProfitPerMinute(displayMode, logisticTime))

class ComponentComplexit(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentLogisticSteps(displayMode, logisticTime))
        self.AddColumn(ComponentProductionSteps(displayMode, logisticTime))
        self.AddColumn(ComponentComplexity(displayMode, logisticTime))
        self.AddColumn(ComponentsPerMinute(displayMode, logisticTime))
        self.AddColumn(ComponentSellPrice(displayMode, logisticTime))
        self.AddColumn(ComponentProfit(displayMode, logisticTime))
        self.AddColumn(ComponentProfitability(displayMode, logisticTime))

class ComponentDataMinute(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentSellPrice(displayMode, logisticTime))
        self.AddColumn(ComponentProfitability(displayMode, logisticTime))
        self.AddColumn(ComponentsPerMinute(displayMode, logisticTime))
        self.AddColumn(ComponentCostPerMinute(displayMode, logisticTime))
        self.AddColumn(ComponentProfitPerMinute(displayMode, logisticTime))
        self.AddColumn(ComponentIncomePerMinute(displayMode, logisticTime))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime))

class ComponentDataHour(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentSellPrice(displayMode, logisticTime))
        self.AddColumn(ComponentProfitability(displayMode, logisticTime))
        self.AddColumn(ComponentsPerHour(displayMode, logisticTime))
        self.AddColumn(ComponentCostPerHour(displayMode, logisticTime))
        self.AddColumn(ComponentProfitPerHour(displayMode, logisticTime))
        self.AddColumn(ComponentIncomePerHour(displayMode, logisticTime))
        self.AddColumn(ModuleDataYieldPerHour(displayMode, logisticTime))

class DataYieldOverview(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ModuleDataYield(displayMode, logisticTime))
        self.AddColumn(ComponentsPerMinute(displayMode, logisticTime))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime))
        self.AddColumn(ComponentCosts(displayMode, logisticTime))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime))

class DataYieldBalanceDetails(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "groundwork"))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "mechanics"))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "electronics"))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "power"))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "hydraulics"))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "precision mechanics"))
        self.AddColumn(ModuleDataYield(displayMode, logisticTime, "heavy machinery"))

class DataYieldCostDetails(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentCosts(displayMode, logisticTime))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "groundwork"))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "mechanics"))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "electronics"))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "power"))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "hydraulics"))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "precision mechanics"))
        self.AddColumn(ModuleDataYieldCost(displayMode, logisticTime, "heavy machinery"))

class DataYieldRateDetails(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, Module.objects.all()[limitFrom:limitTo])
        self.AddColumn(ComponentsPerMinute(displayMode, logisticTime))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "groundwork"))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "mechanics"))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "electronics"))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "power"))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "hydraulics"))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "precision mechanics"))
        self.AddColumn(ModuleDataYieldPerMinute(displayMode, logisticTime, "heavy machinery"))


def formatCellText(text):
    return "<span style='font-family: courier; font-size: small; font-weight:bold;'>" + text.replace(" ", "&nbsp;") + "</span>"

def formatCellSubText(text):
    return "<span style='font-family: courier; font-size: smaller;'>" + text.replace(" ", "&nbsp;") + "</span>"

#region Complexity

def getComplexityString(isOpt = True):
    if isOpt:
        return "<span style='font-family: courier; font-size: smaller;'>Optm: </span>"
    else:
        return "<span style='font-family: courier; font-size: smaller;'>Smpl: </span>"

#region Complexity Functions
def getComponentLogisticSteps(module, materials, useUniqueSteps = False):
    steps = 0
    for inputMat in module.InputMaterials.all():
        if inputMat.id not in materials and useUniqueSteps:
            materials.append(inputMat.id)
            materialQuery = Module.objects.filter(Material=inputMat.Material)
            if materialQuery.exists():
                steps += getComponentLogisticSteps(materialQuery.all()[0], materials, useUniqueSteps)
            else:
                steps += 1
        if not useUniqueSteps:
            steps += 1
            materialQuery = Module.objects.filter(Material=inputMat.Material)
            if materialQuery.exists():
                steps += getComponentLogisticSteps(materialQuery.all()[0], materials, useUniqueSteps)
    return steps

def getComponentProductionSteps(module, getFullSteps = False):
    if getFullSteps:
        steps = 1.0
    else:
        steps = 1.0 / module.OutputAmount
    for inputMat in module.InputMaterials.all():
        moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
        if moduleMatQuery.exists():
            steps += getComponentProductionSteps(moduleMatQuery.all()[0], getFullSteps) * inputMat.Amount
    return steps

def getComponentComplexity(module, getOptimizedValue = False):
    complexityLogisticsWeight = 0.6
    value = 0
    if getOptimizedValue:
        value = getComponentProductionSteps(module, False) * (1.0 - complexityLogisticsWeight) + getComponentLogisticSteps(module, [], True) * complexityLogisticsWeight
    else:
        value = getComponentProductionSteps(module, True) * (1.0 - complexityLogisticsWeight) + getComponentLogisticSteps(module, [], False) * complexityLogisticsWeight
    return value ** 0.33
#endregion

#region Complexity Fields
class ComponentLogisticSteps(ColumnBase):
    def GetHeader(self):
        return "Logistic Steps"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            all = getComponentLogisticSteps(module, [], False)
            unique = getComponentLogisticSteps(module, [], True)
            if (self.displayMode == 2 and all != unique) or self.displayMode == 3:
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (all))) + "<br>" +
                        getComplexityString(True) + formatCellText(str("%4.0f" % (unique))))

            if self.displayMode == 0 or (self.displayMode == 2 and all == unique):
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (all))))

            if self.displayMode == 1:
                rows.append(getComplexityString(True) + formatCellText(str("%4.0f" % (unique))))
        return rows

class ComponentProductionSteps(ColumnBase):
    def GetHeader(self):
        return "Production Steps"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            full = getComponentProductionSteps(module, True)
            part = getComponentProductionSteps(module, False)
            if (self.displayMode == 2 and full != part) or self.displayMode == 3:
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (full))+"  ") + "<br>" +
                        getComplexityString(True) + formatCellText(str("%6.1f" % (part))))
            if self.displayMode == 0 or (self.displayMode == 2 and full == part):
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (full))+"  "))
            if self.displayMode == 1:
                rows.append(getComplexityString(True) + formatCellText(str("%6.1f" % (part))))
        return rows

class ComponentComplexity(ColumnBase):
    def GetHeader(self):
        return "Complexity"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            full = getComponentComplexity(module, False)
            optimized = getComponentComplexity(module, True)
            if (self.displayMode == 2 and full != optimized) or self.displayMode == 3:
                rows.append(getComplexityString(False) + formatCellText(str("%6.2f" % (full))) + "<br>" +
                        getComplexityString(True) + formatCellText(str("%6.2f" % (optimized))))
            if self.displayMode == 0 or (self.displayMode == 2 and full == optimized):
                rows.append(getComplexityString(False) + formatCellText(str("%6.2f" % (full))))
            if self.displayMode == 1:
                rows.append(getComplexityString(True) + formatCellText(str("%6.2f" % (optimized))))
        return rows
#endregion
#endregion

#region Module Data
def getBatchString(module, getBatch = True):
    if getBatch:
        return "<span style='font-family: courier; font-size: smaller;'>bt("+str("%2.0f" % module.OutputAmount)+"): </span>"
    else:
        return "<span style='font-family: courier; font-size: smaller;'>ea( 1): </span>"

class ComponentBatches(ColumnBase):
    def GetHeader(self):
        return "Batch"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%.0f" % module.OutputAmount)))
        return rows
#endregion

#region Finances
def employeeCostPerComponent(module, handlingtime):
    return employeeCostPerSecond() * getComponentCraftingTime(module, handlingtime, True)

def totalCostPerComponent(module, handlingtime):
    return employeeCostPerComponent(module, handlingtime) + module.rawMaterialCost()

def totalProfitPerComponent(module, handlingtime):
    return (module.BaseMarketPrice / module.OutputAmount) - totalCostPerComponent(module, handlingtime)

def getComponentProfitability(module, handlingtime):
    totalCosts = totalCostPerComponent(module, handlingtime)
    return ((module.BaseMarketPrice - totalCosts) / totalCosts) * 100


class ComponentMaterialCosts(ColumnBase):
    def GetHeader(self):
        return "Material Costs"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            if (self.displayMode == 2 and module.OutputAmount > 1) or self.displayMode == 3:
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (module.rawMaterialCost() * module.OutputAmount))) + "<br>" +
                        getBatchString(module, False) + formatCellText(str("%6.0f" % (module.rawMaterialCost()))))
            if self.displayMode == 0 or (self.displayMode == 2 and module.OutputAmount == 1):
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (module.rawMaterialCost() * module.OutputAmount))))
            if self.displayMode == 1:
                rows.append(getBatchString(module, False) + formatCellText(str("%6.0f" % (module.rawMaterialCost()))))
        return rows

class ComponentEmployeeCosts(ColumnBase):
    def GetHeader(self):
        return "Employee Costs"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            employeeCosts = employeeCostPerComponent(module, self.logisticsTime)
            if (self.displayMode == 2 and module.OutputAmount > 1) or self.displayMode == 3:
                rows.append(getBatchString(module, True) + formatCellText(str("%5.0f" % (employeeCosts * module.OutputAmount))) + "<br>" +
                    getBatchString(module, False) + formatCellText(str("%5.0f" % (employeeCosts))))
            if self.displayMode == 0 or (self.displayMode == 2 and module.OutputAmount == 1):
                rows.append(getBatchString(module, True) + formatCellText(str("%5.0f" % (employeeCosts * module.OutputAmount))))
            if self.displayMode == 1:
                rows.append(getBatchString(module, False) + formatCellText(str("%5.0f" % (employeeCosts))))
        return rows

class ComponentCosts(ColumnBase):
    def GetHeader(self):
        return "Component Costs"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            totalCosts = totalCostPerComponent(module, self.logisticsTime)
            if (self.displayMode == 2 and module.OutputAmount > 1) or self.displayMode == 3:
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (totalCosts * module.OutputAmount))) + "<br>" +
                    getBatchString(module, False) + formatCellText(str("%6.0f" % (totalCosts))))
            if self.displayMode == 0 or (self.displayMode == 2 and module.OutputAmount == 1):
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (totalCosts * module.OutputAmount))))
            if self.displayMode == 1:
                rows.append(getBatchString(module, False) + formatCellText(str("%6.0f" % (totalCosts))))
        return rows

class ComponentSellPrice(ColumnBase):
    def GetHeader(self):
        return "Sell Price"

    def IsEditable(self):
        if self.displayMode == 1:
            return True
        else:
            return False

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            if (self.displayMode == 2 and module.OutputAmount > 1) or self.displayMode == 3:
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (module.BaseMarketPrice))) + "<br>" +
                    getBatchString(module, False) + formatCellText(str("%6.0f" % (module.BaseMarketPrice / module.OutputAmount))))
            if self.displayMode == 0 or (self.displayMode == 2 and module.OutputAmount == 1):
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (module.BaseMarketPrice / module.OutputAmount))))
            if self.displayMode == 1:
                rows.append(module.BaseMarketPrice / module.OutputAmount)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        module.BaseMarketPrice = float(value) * module.OutputAmount
        module.save()

class ComponentProfit(ColumnBase):
    def GetHeader(self):
        return "Profit"

    def IsEditable(self):
        if self.displayMode == 1 and self.logisticsTime == 0:
            return True
        else:
            return False

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            profit = totalProfitPerComponent(module, self.logisticsTime)
            if (self.displayMode == 2 and module.OutputAmount > 1) or self.displayMode == 3:
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (profit * module.OutputAmount))) + "<br>" +
                    getBatchString(module, False) + formatCellText(str("%6.0f" % (profit))))
            if self.displayMode == 0 or (self.displayMode == 2 and module.OutputAmount == 1):
                rows.append(getBatchString(module, True) + formatCellText(str("%6.0f" % (profit * module.OutputAmount))))
            if self.displayMode == 1 and self.logisticsTime > 0:
                rows.append(getBatchString(module, False) + formatCellText(str("%6.0f" % (profit))))
            if self.displayMode == 1 and self.logisticsTime == 0:
                rows.append(profit)
        return rows

    def SetValue(self, objID, value):
        module = Module.objects.get(id=objID)
        module.BaseMarketPrice = (float(value) + totalCostPerComponent(module)) * module.OutputAmount
        module.save()

class ComponentProfitability(ColumnBase):
    def GetHeader(self):
        return "Profitability"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%5.0f" % (getComponentProfitability(module, self.logisticsTime))) + "%"))
        return rows
#endregion

#region Time Based Data
def getComponentCraftingTime(module, handlingtime = 0, fullProductionLine = True):
    totalTime = 0
    if fullProductionLine:
        for inputMat in module.InputMaterials.all():
            moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
            if moduleMatQuery.exists():
                totalTime += getComponentCraftingTime(moduleMatQuery.all()[0], handlingtime) * inputMat.Amount
    craftingDuration = CrafterPropertyModuleDuration.objects.filter(Module=module).order_by("id")
    if craftingDuration.exists():
        totalTime += (craftingDuration.all()[0].Duration + handlingtime) / module.OutputAmount
        return totalTime
    else:
        return 0

#region Time Based Values
def daysPerSecond():
    return 1.0 / float(TuningValue.objects.get(Name="SecondsPerDay").Value)

def componentsPerSecond(module, handlingtime):
    craftingtime = getComponentCraftingTime(module, handlingtime, False)
    if (craftingtime > 0):
        return (1.0 / craftingtime)
    else:
        return 0

def employeeCostPerSecond():
    return daysPerSecond() * float(TuningValue.objects.get(Name="EmployeeWage").Value)

def componentCostsPerSecond(module, handlingtime = 0):
    craftingtime = getComponentCraftingTime(module, handlingtime, False)
    if (craftingtime > 0):
        return totalCostPerComponent(module, handlingtime) / craftingtime
    else:
        return 0

def componentIncomePerSecond(module, handlingtime = 0):
    craftingtime = getComponentCraftingTime(module, handlingtime, False)
    if (craftingtime > 0):
        return module.BaseMarketPrice / (craftingtime * module.OutputAmount)
    else:
        return 0

def componentProfitPerSecond(module, handlingtime = 0):
    craftingtime = getComponentCraftingTime(module, handlingtime, False)
    if (craftingtime > 0):
        return totalProfitPerComponent(module, handlingtime) / craftingtime
    else:
        return 0
#endregion

class ComponentCraftingTime(ColumnBase):
    def GetHeader(self):
        return "Time"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            craftingDuration = getComponentCraftingTime(module, self.logisticsTime)
            if (self.displayMode == 2 and module.OutputAmount > 1) or self.displayMode == 3:
                rows.append(getBatchString(module, True) + formatCellText(str("%5.0f" %(craftingDuration))+"  ") + "<br>" +
                    getBatchString(module, False) + formatCellText(str("%7.1f" %(craftingDuration / module.OutputAmount))))
            if self.displayMode == 0 or (self.displayMode == 2 and module.OutputAmount == 1):
                rows.append(getBatchString(module, True) + formatCellText(str("%5.0f" %(craftingDuration))+"  "))
            if self.displayMode == 1:
                rows.append(getBatchString(module, False) + formatCellText(str("%7.1f" %(craftingDuration / module.OutputAmount))))
        return rows

class ComponentCostPerMinute(ColumnBase):
    def GetHeader(self):
        return "Cost Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%8.0f" %(componentCostsPerSecond(module, self.logisticsTime) * 60))))
        return rows

class ComponentCostPerHour(ColumnBase):
    def GetHeader(self):
        return "Cost Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%8.0f" %(componentCostsPerSecond(module, self.logisticsTime) * 3600))))
        return rows

class ComponentProfitPerMinute(ColumnBase):
    def GetHeader(self):
        return "Profit Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%8.0f" %(componentProfitPerSecond(module, self.logisticsTime) * 60))))
        return rows

class ComponentProfitPerHour(ColumnBase):
    def GetHeader(self):
        return "Profit Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%8.0f" %(componentProfitPerSecond(module, self.logisticsTime) * 3600))))
        return rows

class ComponentIncomePerMinute(ColumnBase):
    def GetHeader(self):
        return "Income Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%8.0f" %(componentIncomePerSecond(module, self.logisticsTime) * 60))))
        return rows

class ComponentIncomePerHour(ColumnBase):
    def GetHeader(self):
        return "Income Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            rows.append(formatCellText(str("%8.0f" %(componentIncomePerSecond(module, self.logisticsTime) * 3600))))
        return rows

class ComponentsPerMinute(ColumnBase):
    def GetHeader(self):
        return "Components Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            craftingtime = getComponentCraftingTime(module, self.logisticsTime, False)
            if (craftingtime > 0):
                rows.append(formatCellText(str("%7.1f" %((1.0 / craftingtime) * 60))))
            else:
                rows.append(formatCellText("N/A"))
        return rows

class ComponentsPerHour(ColumnBase):
    def GetHeader(self):
        return "Components Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            craftingtime = getComponentCraftingTime(module, self.logisticsTime, False)
            if (craftingtime > 0):
                rows.append(formatCellText(str("%7.1f" %((1.0 / craftingtime) * 3600))))
            else:
                rows.append(formatCellText("N/A"))
        return rows
#endregion

#region Research

def getComponentDataYield(module, datatype):
    dataTypeQuery = ResearchDataType.objects.filter(Name=datatype)
    if dataTypeQuery.exists():
        dataQuery = ModuleResearchDataYield.objects.filter(Module=module, ResearchDataType=dataTypeQuery.all()[0])
        if dataQuery.exists():
            return dataQuery.all()[0].Amount
        else:
            return 0
    else:
        return 0

class ModuleDataYield(ColumnBase):
    def GetHeader(self):
        if self.option == "":
            return "Data Yield"
        else:
            return self.option


    def GetRowStrings(self, query):
        rows = []

        for module in query.all():
            string = ""
            if self.option == "":
                row = 0
                dataTypeQuery = module.ResearchDataYield
                if dataTypeQuery.exists():
                    for dataType in dataTypeQuery.all():
                        if row > 0:
                            string += "<br>"
                        row += 1
                        string += formatCellSubText(((dataType.ResearchDataType.Name[:10]) + ": ").ljust(12))
                        string += formatCellText(str("%4.0f" % dataType.Amount))
                    rows.append(string)
                else:
                    rows.append(formatCellText("N/A"))
            else:
                dataYield = getComponentDataYield(module, self.option)
                if dataYield == 0:
                    rows.append(formatCellText(""))
                else:
                    rows.append(formatCellText(str("%4.0f" % (dataYield))))
        return rows

class ModuleDataYieldPerMinute(ColumnBase):
    def GetHeader(self):
        if self.option == "":
            return "Data Yield per Minute"
        else:
            return self.option+" per Minute"


    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            string = ""
            componentsPerMinute = (componentsPerSecond(module, self.logisticsTime) * 60)
            if self.option == "":
                row = 0
                dataTypeQuery = module.ResearchDataYield
                if dataTypeQuery.exists():
                    for dataType in dataTypeQuery.all():
                        if row > 0:
                            string += "<br>"
                        row += 1
                        string += formatCellSubText(((dataType.ResearchDataType.Name[:10]) + ": ").ljust(12))
                        string += formatCellText(str("%4.0f" % (float(dataType.Amount) * componentsPerMinute)))
                    rows.append(string)
                else:
                    rows.append(formatCellText("N/A"))
            else:
                dataYield = getComponentDataYield(module, self.option)
                if dataYield == 0:
                    rows.append(formatCellText(""))
                else:
                    rows.append(formatCellText(str("%4.0f" % (dataYield * componentsPerMinute))))
        return rows

class ModuleDataYieldPerHour(ColumnBase):
    def GetHeader(self):
        if self.option == "":
            return "Data Yield per Hour"
        else:
            return self.option+" per Hour"


    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            string = ""
            componentsPerHour = ((componentsPerSecond(module, self.logisticsTime) * 3600))
            if self.option == "":
                row = 0
                dataTypeQuery = module.ResearchDataYield
                if dataTypeQuery.exists():
                    for dataType in dataTypeQuery.all():
                        if row > 0:
                            string += "<br>"
                        row += 1
                        string += formatCellSubText(((dataType.ResearchDataType.Name[:10]) + ": ").ljust(12))
                        string += formatCellText(str("%4.0f" % (dataType.Amount * componentsPerHour)))
                    rows.append(string)
                else:
                    rows.append(formatCellText("N/A"))
            else:
                dataYield = getComponentDataYield(module, self.option)
                if dataYield == 0:
                    rows.append(formatCellText(""))
                else:
                    rows.append(formatCellText(str("%4.0f" % (dataYield * componentsPerHour))))
        return rows

class ModuleDataYieldCost(ColumnBase):
    def GetHeader(self):
        if self.option == "":
            return "Data Yield Cost"
        else:
            return self.option+" Cost"


    def GetRowStrings(self, query):
        rows = []
        for module in query.all():
            string = ""
            totalCosts = totalCostPerComponent(module, self.logisticsTime)
            if self.option == "":
                row = 0
                dataTypeQuery = module.ResearchDataYield
                if dataTypeQuery.exists():
                    for dataType in dataTypeQuery.all():
                        if row > 0:
                            string += "<br>"
                        row += 1
                        string += formatCellSubText(((dataType.ResearchDataType.Name[:10]) + ": ").ljust(12))
                        string += formatCellText(str("%4.0f" % (totalCosts / float(dataType.Amount))))
                    rows.append(string)
                else:
                    rows.append(formatCellText("N/A"))
            else:
                dataYield = getComponentDataYield(module, self.option)
                if dataYield == 0:
                    rows.append(formatCellText(""))
                else:
                    rows.append(formatCellText(str("%4.0f" % (totalCosts /dataYield))))
        return rows

#endregion