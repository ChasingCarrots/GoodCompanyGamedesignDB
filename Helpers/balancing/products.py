from balancingtablebase import *
from Production.models import *
from ObjectTypes.models import *
from Tuning.models import *
from BalancingHelper.models import *
from modules import getModuleTotalProductionTime, getModuleNumProductionSteps, getModuleNumMaterialSteps, getModuleNumUniqueMaterialSteps

extraTimePerBatch = 5.0

class ProductNumProductionSteps(ColumnBase):
    def GetHeader(self):
        return "Production Steps"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            steps = 0
            for module in product.Modules.all():
                steps += getModuleNumProductionSteps(module)
            rows.append("%.2f" % steps)
        return rows

class ProductNumLogisticSteps(ColumnBase):
    def GetHeader(self):
        return "Logistic Steps"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            steps = 0
            for module in product.Modules.all():
                steps += getModuleNumMaterialSteps(module)
            rows.append(steps)
        return rows

class ProductNumUnqiueLogisticSteps(ColumnBase):
    def GetHeader(self):
        return "Unique Logistic Steps"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            materials = []
            steps = 0
            for module in product.Modules.all():
                steps += getModuleNumUniqueMaterialSteps(module, materials)
            rows.append(steps)
        return rows

class ProductNumProductionComplexity(ColumnBase):
    def GetHeader(self):
        return "Production Complexity"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            stepsMods = 0
            stepsMats = 0
            highestMods = 0
            highestMats = 0
            for module in product.Modules.all():
                steps = getModuleNumProductionSteps(module)
                stepsMods += steps
                if steps > highestMods:
                    highestMods = steps
                steps = getModuleNumMaterialSteps(module)
                stepsMats += steps
                if steps > highestMats:
                    highestMats = steps
            rows.append("%.2f" % (((highestMods*0.3 + highestMats*0.7)**0.3 + (stepsMats*0.3 + stepsMods*0.7)**0.7) * 0.25))
        return rows


class ProductNumProductionComplexity2(ColumnBase):
    def GetHeader(self):
        return "Unique Production Complexity"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            materials = []
            stepsMods = 0
            stepsMats = 0
            highestMods = 0
            highestMats = 0
            for module in product.Modules.all():
                steps = getModuleNumProductionSteps(module)
                stepsMods += steps
                if steps > highestMods:
                    highestMods = steps
                steps = getModuleNumUniqueMaterialSteps(module, materials)
                stepsMats += steps
                if steps > highestMats:
                    highestMats = steps
            rows.append("%.2f" % (((highestMods*0.3 + highestMats*0.7)**0.3 + (stepsMats*0.3 + stepsMods*0.7)**0.7) * 0.25))
        return rows

class ProductMaterialCostColumn(ColumnBase):
    def GetHeader(self):
        return "Total Material Cost"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            price = 0
            for module in product.Modules.all():
                price += module.rawMaterialCost()
            rows.append("%.2f" % price)
        return rows


class ProductEmployeeCostColumn(ColumnBase):
    def GetHeader(self):
        return "Total Employee Cost"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeCostsPerDay = float(TuningValue.objects.get(Name="EmployeeWage").Value)
        rows = []
        for product in query.all():
            totalTime = 0
            if product.ProductFunction.ViableProductTypes.exists():
                assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(ProductType=product.ProductFunction.ViableProductTypes.all()[0])
                if assemblyDuration.exists():
                    totalTime = assemblyDuration.all()[0].Duration
                    for module in product.Modules.all():
                        totalTime += getModuleTotalProductionTime(module, extraTimePerBatch)
            rows.append("%.2f" % ((totalTime / secondsPerDay) * employeeCostsPerDay))
        return rows

class ProductProductionTime(ColumnBase):
    def GetHeader(self):
        return "Total Time"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            totalTime = 0
            if product.ProductFunction.ViableProductTypes.exists():
                assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(ProductType=product.ProductFunction.ViableProductTypes.all()[0])
                if assemblyDuration.exists():
                    totalTime = assemblyDuration.all()[0].Duration
                    for module in product.Modules.all():
                        totalTime += getModuleTotalProductionTime(module, extraTimePerBatch)
            rows.append("%.2f" % ((totalTime)))
        return rows


class ProductTotalProductionTimeColumn(ColumnBase):
    def GetHeader(self):
        return "Total production time"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            totalTime = 0
            if product.ProductFunction.ViableProductTypes.exists():
                assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(ProductType=product.ProductFunction.ViableProductTypes.all()[0])
                if assemblyDuration.exists():
                    totalTime = assemblyDuration.all()[0].Duration
                    for module in product.Modules.all():
                        totalTime += getModuleTotalProductionTime(module, extraTimePerBatch)
            rows.append("%.2f" % totalTime)
        return rows

class ProductFunctionBaseMarketPrice(ColumnBase):
    def GetHeader(self):
        return "Sellprice"

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

class ModulesSellPriceSum(ColumnBase):
    def GetHeader(self):
        return "Raw Module Value"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            totalSellPrice = 0
            for module in product.Modules.all():
                totalSellPrice += module.BaseMarketPrice

            rows.append("%.2f" % totalSellPrice)
        return rows

class ProductValueRatio(ColumnBase):
    def GetHeader(self):
        return "Module/Product Price Ration"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            totalSellPrice = 0
            for module in product.Modules.all():
                totalSellPrice += module.BaseMarketPrice

            rows.append("%.2f" % (product.ProductFunction.BaseMarketPrice / totalSellPrice))
        return rows

    def SetValue(self, objID, value):
        product = SampleProduct.objects.get(id=objID)

        totalSellPrice = 0
        for module in product.Modules.all():
             totalSellPrice += module.BaseMarketPrice

        product.ProductFunction.BaseMarketPrice = float(value) * totalSellPrice
        product.ProductFunction.save()

class ProductProductionCostPerProduct(ColumnBase):
    def GetHeader(self):
        return "Cost/Product"

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for product in query.all():
            totalRawMaterialCost = 0

            assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
                ProductType=product.ProductFunction.ViableProductTypes.all()[0])
            if assemblyDuration.exists():
                totalProductionTime = assemblyDuration.all()[0].Duration
            else:
                rows.append("no assembly")
                continue

            for module in product.Modules.all():
                totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
                totalRawMaterialCost += module.rawMaterialCost()

            totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond
            rows.append("%.2f" % totalProductionCosts)
        return rows


class ProductProfitPerProduct(ColumnBase):
    def GetHeader(self):
        return "Profit/Product"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for product in query.all():
            totalRawMaterialCost = 0

            assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
                ProductType=product.ProductFunction.ViableProductTypes.all()[0])
            if assemblyDuration.exists():
                totalProductionTime = assemblyDuration.all()[0].Duration
            else:
                rows.append("no assembly")
                continue

            for module in product.Modules.all():
                totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
                totalRawMaterialCost += module.rawMaterialCost()

            totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond
            rows.append("%.2f" % (product.ProductFunction.BaseMarketPrice - totalProductionCosts))
        return rows

    def SetValue(self, objID, value):
        product = SampleProduct.objects.get(id=objID)
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay

        totalRawMaterialCost = 0

        assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
            ProductType=product.ProductFunction.ViableProductTypes.all()[0])
        if assemblyDuration.exists():
            totalProductionTime = assemblyDuration.all()[0].Duration

        for module in product.Modules.all():
            totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
            totalRawMaterialCost += module.rawMaterialCost()

        totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond


        product.ProductFunction.BaseMarketPrice = float(value) + totalProductionCosts
        product.ProductFunction.save()



class ProductProfitPerDay(ColumnBase):
    def GetHeader(self):
        return "Profit/Day"


    def IsEditable(self):
        return False

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for product in query.all():
            totalRawMaterialCost = 0

            assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(ProductType=product.ProductFunction.ViableProductTypes.all()[0])
            if assemblyDuration.exists():
                totalProductionTime = assemblyDuration.all()[0].Duration
            else:
                rows.append("no assembly")
                continue

            for module in product.Modules.all():
                totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
                totalRawMaterialCost += module.rawMaterialCost()

            sellPrice = product.ProductFunction.BaseMarketPrice
            totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond
            profitPerProduct = sellPrice - totalProductionCosts
            profitPerDay = secondsPerDay * (profitPerProduct / totalProductionTime)
            rows.append("%.2f" % profitPerDay)
        return rows

    def SetValue(self, objID, value):
        product = SampleProduct.objects.get(id=objID)
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay

        totalRawMaterialCost = 0

        assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
            ProductType=product.ProductFunction.ViableProductTypes.all()[0])
        if assemblyDuration.exists():
            totalProductionTime = assemblyDuration.all()[0].Duration

        for module in product.Modules.all():
            totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
            totalRawMaterialCost += module.rawMaterialCost()

        #sellPrice = product.ProductFunction.BaseMarketPrice
        totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond
        #profitPerProduct = sellPrice - totalProductionCosts
        #profitPerDay = secondsPerDay * (profitPerProduct / totalProductionTime)

        #module.BaseMarketPrice = float(value) / (secondsPerDay / productionTime) + productionCost


        product.ProductFunction.BaseMarketPrice = float(value) / (secondsPerDay / totalProductionTime) + totalProductionCosts
        product.ProductFunction.save()

class ProductProfitability(ColumnBase):
    def GetHeader(self):
        return "Profitability"

    def IsEditable(self):
        return True

    def GetRowStrings(self, query):
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay
        rows = []
        for product in query.all():
            totalRawMaterialCost = 0

            assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
                ProductType=product.ProductFunction.ViableProductTypes.all()[0])
            if assemblyDuration.exists():
                totalProductionTime = assemblyDuration.all()[0].Duration
            else:
                rows.append("no assembly")
                continue

            for module in product.Modules.all():
                totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
                totalRawMaterialCost += module.rawMaterialCost()

            totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond

            if totalProductionTime == 0:
                rows.append("err")
            else:
                rows.append("%.2f" % (product.ProductFunction.BaseMarketPrice/totalProductionCosts))
        return rows


    def SetValue(self, objID, value):
        product = SampleProduct.objects.get(id=objID)
        secondsPerDay = float(TuningValue.objects.get(Name="SecondsPerDay").Value)
        employeeWagePerSecond = float(TuningValue.objects.get(Name="EmployeeWage").Value) / secondsPerDay

        totalRawMaterialCost = 0

        assemblyDuration = AssemblyPropertyProductTypeAssemblyDuration.objects.filter(
            ProductType=product.ProductFunction.ViableProductTypes.all()[0])
        if assemblyDuration.exists():
            totalProductionTime = assemblyDuration.all()[0].Duration

        for module in product.Modules.all():
            totalProductionTime += getModuleTotalProductionTime(module, extraTimePerBatch)
            totalRawMaterialCost += module.rawMaterialCost()

        totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond


        product.ProductFunction.BaseMarketPrice = float(value) * totalProductionCosts
        product.ProductFunction.save()

class ProductBalancingTable(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        #self.AddColumn(ProductNumProductionSteps())
        #self.AddColumn(ProductNumLogisticSteps())
        #self.AddColumn(ProductNumProductionComplexity())
        #self.AddColumn(ProductProductionTime())
        self.AddColumn(ProductNumProductionComplexity2())
        #self.AddColumn(ProductEmployeeCostColumn())
        #self.AddColumn(ProductTotalProductionTimeColumn())
        self.AddColumn(ProductMaterialCostColumn())
        self.AddColumn(ProductProductionCostPerProduct())
        self.AddColumn(ModulesSellPriceSum())
        self.AddColumn(ProductFunctionBaseMarketPrice())
        self.AddColumn(ProductValueRatio())
        self.AddColumn(ProductProfitPerProduct())
        self.AddColumn(ProductProfitPerDay())
        self.AddColumn(ProductProfitability())

class ProductProductionOverview(BalancingTableBase):
    def __init__(self, limitFrom, limitTo, displayMode = 0, logisticTime = 0):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductNumProductionSteps())
        self.AddColumn(ProductNumLogisticSteps())
        self.AddColumn(ProductNumUnqiueLogisticSteps())
        self.AddColumn(ProductNumProductionComplexity())
        self.AddColumn(ProductNumProductionComplexity2())
        self.AddColumn(ProductProductionTime())
        #self.AddColumn(ProductEmployeeCostColumn())
        #self.AddColumn(ProductTotalProductionTimeColumn())
        self.AddColumn(ProductMaterialCostColumn())
        self.AddColumn(ProductProductionCostPerProduct())
        #self.AddColumn(ProductFunctionBaseMarketPrice())
        self.AddColumn(ProductProfitPerProduct())
        #self.AddColumn(ProductProfitPerDay())
        self.AddColumn(ProductProfitability())