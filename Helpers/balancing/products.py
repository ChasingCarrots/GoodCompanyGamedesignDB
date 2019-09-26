from balancingtablebase import *
from Production.models import *
from ObjectTypes.models import *
from Tuning.models import *
from BalancingHelper.models import *
from modules import employeeCostPerComponent, totalCostPerComponent, formatCellText, getComponentCraftingTime, getComponentLogisticSteps, getComponentProductionSteps, getComplexityString


class ProductBalancing(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0, option = None):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductModuleAmount(displayMode, logisticTime))
        self.AddColumn(ProductComplexity(displayMode, logisticTime))
        self.AddColumn(ProductCost(displayMode, logisticTime))
        self.AddColumn(ModuleSellPriceSum(displayMode, logisticTime))
        self.AddColumn(ProductValueRatio(displayMode, logisticTime))
        self.AddColumn(ProductPrice(displayMode, logisticTime))
        self.AddColumn(ProductProfit(displayMode, logisticTime))
        self.AddColumn(ProductProfitability(displayMode, logisticTime))

class ProductFinances(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0, option = None):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductsPerMinute(displayMode, logisticTime))
        self.AddColumn(ProductMaterialCost(displayMode, logisticTime))
        self.AddColumn(ProductEmployeeCost(displayMode, logisticTime))
        self.AddColumn(ProductPrice(displayMode, logisticTime))
        self.AddColumn(ProductProfit(displayMode, logisticTime))
        self.AddColumn(ProductProfitability(displayMode, logisticTime))
        self.AddColumn(ProductProfitPerMinute(displayMode, logisticTime))

class ProductComplexit(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0, option = None):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductModuleAmount(displayMode, logisticTime))
        self.AddColumn(ProductLogisticSteps(displayMode, logisticTime))
        self.AddColumn(ProductProductionSteps(displayMode, logisticTime))
        self.AddColumn(ProductComplexity(displayMode, logisticTime))
        self.AddColumn(ProductsPerMinute(displayMode, logisticTime))
        self.AddColumn(ProductPrice(displayMode, logisticTime))
        self.AddColumn(ProductProfit(displayMode, logisticTime))
        self.AddColumn(ProductProfitability(displayMode, logisticTime))

class ProductDataMinute(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0, option = None):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductPrice(displayMode, logisticTime))
        self.AddColumn(ProductProfitability(displayMode, logisticTime))
        self.AddColumn(ProductsPerMinute(displayMode, logisticTime))
        self.AddColumn(ProductCostPerMinute(displayMode, logisticTime))
        self.AddColumn(ProductProfitPerMinute(displayMode, logisticTime))
        self.AddColumn(ProductIncomePerMinute(displayMode, logisticTime))

class ProductDataHour(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0, option = None):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductPrice(displayMode, logisticTime))
        self.AddColumn(ProductProfitability(displayMode, logisticTime))
        self.AddColumn(ProductsPerHour(displayMode, logisticTime))
        self.AddColumn(ProductCostPerHour(displayMode, logisticTime))
        self.AddColumn(ProductProfitPerHour(displayMode, logisticTime))
        self.AddColumn(ProductIncomePerHour(displayMode, logisticTime))

#region complexity
def getModuleAmount(product):
    modules = 0
    for module in product.Modules.all():
        modules += 1
    return modules

def getProductComplexity(product, getOptimizedValue = False):
    complexityLogisticsWeight = 0.6
    productionSteps = 0
    logisticSteps = 0
    materials = []
    value = 0

    if getOptimizedValue:
        for module in product.Modules.all():
            productionSteps += getComponentProductionSteps(module, False)
            logisticSteps += getComponentLogisticSteps(module, materials, True)
        value = productionSteps * (1.0 - complexityLogisticsWeight) + logisticSteps * complexityLogisticsWeight
    else:
        for module in product.Modules.all():
            productionSteps += getComponentProductionSteps(module, True)
            logisticSteps += getComponentLogisticSteps(module, materials, False)
        value = productionSteps * (1.0 - complexityLogisticsWeight) + logisticSteps * complexityLogisticsWeight
    return value ** 0.33

class ProductModuleAmount(ColumnBase):
    def GetHeader(self):
        return "Modules"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%2.0f" % (getModuleAmount(product)))))
        return rows

class ProductLogisticSteps(ColumnBase):
    def GetHeader(self):
        return "Logistic Steps"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            all = 0
            unique = 0
            materials = []
            for module in product.Modules.all():
                all += getComponentLogisticSteps(module, [], False)
                unique += getComponentLogisticSteps(module, materials, True)
            if (self.displayMode == 2 and all != unique) or self.displayMode == 3:
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (all))+"  ") + "<br>" +
                        getComplexityString(True) + formatCellText(str("%6.1f" % (unique))))
            if self.displayMode == 0 or (self.displayMode == 2 and all == unique):
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (all))+"  "))
            if self.displayMode == 1:
                rows.append(getComplexityString(True) + formatCellText(str("%6.1f" % (unique))))
        return rows

class ProductProductionSteps(ColumnBase):
    def GetHeader(self):
        return "Production Steps"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            full = 0
            part = 0
            for module in product.Modules.all():
                full += getComponentProductionSteps(module, True)
                part += getComponentProductionSteps(module, False)

            if (self.displayMode == 2 and full != part) or self.displayMode == 3:
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (full))+"  ") + "<br>" +
                        getComplexityString(True) + formatCellText(str("%6.1f" % (part))))
            if self.displayMode == 0 or (self.displayMode == 2 and full == part):
                rows.append(getComplexityString(False) + formatCellText(str("%4.0f" % (full))+"  "))
            if self.displayMode == 1:
                rows.append(getComplexityString(True) + formatCellText(str("%6.1f" % (part))))
        return rows

class ProductComplexity(ColumnBase):
    def GetHeader(self):
        return "Complexity"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            full = getProductComplexity(product)
            optimized = getProductComplexity(product, True)

            if (self.displayMode == 2 and full != optimized) or self.displayMode == 3:
                rows.append(getComplexityString(False) + formatCellText(str("%6.2f" % (full))) + "<br>" +
                        getComplexityString(True) + formatCellText(str("%6.2f" % (optimized))))
            if self.displayMode == 0 or (self.displayMode == 2 and full == optimized):
                rows.append(getComplexityString(False) + formatCellText(str("%6.2f" % (full))))
            if self.displayMode == 1:
                rows.append(getComplexityString(True) + formatCellText(str("%6.2f" % (optimized))))
        return rows
#endregion

#region financial

def materialCostPerProduct(product):
    sum = 0
    for module in product.Modules.all():
        sum += module.rawMaterialCost()
    return sum

def employeeCostPerProduct(product, handlingtime):
    sum = 0
    for module in product.Modules.all():
        sum += employeeCostPerComponent(module, handlingtime)
    return sum

def totalCostPerProduct(product, handlingtime):
    sum = 0
    for module in product.Modules.all():
        sum += totalCostPerComponent(module, handlingtime)
    return sum

def totalProfitPerProduct(product, handlingtime):
    return product.ProductFunction.BaseMarketPrice - totalCostPerProduct(product, handlingtime)

def getProductProfitability(product, handlingtime):
    totalCosts = totalCostPerProduct(product, handlingtime)
    if totalCosts == 0:
        return 0
    return ((product.ProductFunction.BaseMarketPrice - totalCosts) / totalCosts) * 100

def getProductModuleValue(product):
    totalSellPrice = 0
    for module in product.Modules.all():
        totalSellPrice += module.BaseMarketPrice
    return totalSellPrice

class ProductPrice(ColumnBase):
    def GetHeader(self):
        return "Sell Price"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(product.ProductFunction.BaseMarketPrice)
        return rows

    def SetValue(self, objID, value):
        product = SampleProduct.objects.get(id=objID)
        product.ProductFunction.BaseMarketPrice = int(value)
        product.ProductFunction.save()

class ProductMaterialCost(ColumnBase):
    def GetHeader(self):
        return "Material Costs"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%6.0f" % (materialCostPerProduct(product)))))
        return rows

class ProductEmployeeCost(ColumnBase):
    def GetHeader(self):
        return "Employee Costs"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%6.0f" % (employeeCostPerProduct(product, self.logisticsTime)))))
        return rows

class ProductCost(ColumnBase):
    def GetHeader(self):
        return "Costs"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%6.0f" % (totalCostPerProduct(product, self.logisticsTime)))))
        return rows

class ProductProfit(ColumnBase):
    def GetHeader(self):
        return "Profit"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%6.0f" % (totalProfitPerProduct(product, self.logisticsTime)))))
        return rows

class ProductProfitability(ColumnBase):
    def GetHeader(self):
        return "Product Profitability"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%6.0f" % (getProductProfitability(product, self.logisticsTime)))+"%"))
        return rows

class ModuleSellPriceSum(ColumnBase):
    def GetHeader(self):
        return "Module Value"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%7.0f" % getProductModuleValue(product))))
        return rows

class ProductValueRatio(ColumnBase):
    def GetHeader(self):
        return "Module/Product Value"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%7.2f" % (product.ProductFunction.BaseMarketPrice / getProductModuleValue(product)))))
        return rows

#endregion



#region Time Based Data

def getProductCraftingTime(product, handlingtime = 0, fullProductionLine = True):
    totalTime = 0
    assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
        ProductType=product.ProductFunction.ViableProductTypes.all()[0])
    if assemblyDuration.exists():
        totalTime = assemblyDuration.all()[0].Duration
    if fullProductionLine:
        for module in product.Modules.all():
            for inputMat in module.InputMaterials.all():
                moduleMatQuery = Module.objects.filter(Material=inputMat.Material)
                if moduleMatQuery.exists():
                    totalTime += getComponentCraftingTime(moduleMatQuery.all()[0], handlingtime) * inputMat.Amount
    return totalTime

#region Time Based Values

def productCostsPerSecond(product, handlingtime = 0):
    return totalCostPerProduct(product, handlingtime) / getProductCraftingTime(product, handlingtime, False)

def productIncomePerSecond(product, handlingtime = 0):
    return product.ProductFunction.BaseMarketPrice / getProductCraftingTime(product, handlingtime, False)

def productProfitPerSecond(product, handlingtime = 0):
    return totalProfitPerProduct(product, handlingtime) / getProductCraftingTime(product, handlingtime, False)
#endregion

class ProductCraftingTime(ColumnBase):
    def GetHeader(self):
        return "Time"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%6.0f" % (getProductCraftingTime(product, self.logisticsTime, False)))))
        return rows

class ProductCostPerMinute(ColumnBase):
    def GetHeader(self):
        return "Cost Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%8.0f" %(productCostsPerSecond(product, self.logisticsTime) * 60))))
        return rows

class ProductCostPerHour(ColumnBase):
    def GetHeader(self):
        return "Cost Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%8.0f" %(productCostsPerSecond(product, self.logisticsTime) * 3600))))
        return rows

class ProductProfitPerMinute(ColumnBase):
    def GetHeader(self):
        return "Profit Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%8.0f" %(productProfitPerSecond(product, self.logisticsTime) * 60))))
        return rows

class ProductProfitPerHour(ColumnBase):
    def GetHeader(self):
        return "Profit Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%8.0f" %(productProfitPerSecond(product, self.logisticsTime) * 3600))))
        return rows

class ProductIncomePerMinute(ColumnBase):
    def GetHeader(self):
        return "Income Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%8.0f" %(productIncomePerSecond(product, self.logisticsTime) * 60))))
        return rows

class ProductIncomePerHour(ColumnBase):
    def GetHeader(self):
        return "Income Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%8.0f" %(productIncomePerSecond(product, self.logisticsTime) * 3600))))
        return rows

class ProductsPerMinute(ColumnBase):
    def GetHeader(self):
        return "Products Per Minute"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%7.1f" %((1.0 / getProductCraftingTime(product, self.logisticsTime, False)) * 60))))
        return rows

class ProductsPerHour(ColumnBase):
    def GetHeader(self):
        return "Products Per Hour"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            rows.append(formatCellText(str("%7.0f" %((1.0 / getProductCraftingTime(product, self.logisticsTime, False)) * 3600))))
        return rows
#endregion





