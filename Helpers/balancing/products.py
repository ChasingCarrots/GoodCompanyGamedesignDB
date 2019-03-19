from balancingtablebase import *
from Production.models import *
from ObjectTypes.models import *
from Tuning.models import *
from BalancingHelper.models import *
from modules import getModuleTotalProductionTime, getModuleNumProductionSteps

class ProductMaterialCostColumn(ColumnBase):
    def GetHeader(self):
        return "Total Material cost"

    def GetRowStrings(self, query):
        rows = []
        for product in query.all():
            price = 0
            for module in product.Modules.all():
                price += module.rawMaterialCost()
            rows.append("%.2f" % price)
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
                        totalTime += getModuleTotalProductionTime(module)
            rows.append("%.2f" % totalTime)
        return rows

class ProductFunctionBaseMarketPrice(ColumnBase):
    def GetHeader(self):
        return "ProductFunction Sellprice"

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
        product.save()

class ProductProductionCostPerProduct(ColumnBase):
    def GetHeader(self):
        return "Cost per product"

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
                totalProductionTime += getModuleTotalProductionTime(module)
                totalRawMaterialCost += module.rawMaterialCost()

            totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond
            rows.append("%.2f" % totalProductionCosts)
        return rows

class ProductProfitPerDay(ColumnBase):
    def GetHeader(self):
        return "Profit per day"

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
                totalProductionTime += getModuleTotalProductionTime(module)
                totalRawMaterialCost += module.rawMaterialCost()

            sellPrice = product.ProductFunction.BaseMarketPrice
            totalProductionCosts = totalRawMaterialCost + totalProductionTime * employeeWagePerSecond
            profitPerProduct = sellPrice - totalProductionCosts
            profitPerDay = secondsPerDay * (profitPerProduct / totalProductionTime)
            rows.append("%.2f" % profitPerDay)
        return rows

class ProductBalancingTable(BalancingTableBase):
    BalancingTableIdentifier = "Products"
    def __init__(self, limitFrom, limitTo):
        BalancingTableBase.__init__(self, SampleProduct.objects.all()[limitFrom:limitTo])
        self.AddColumn(ProductMaterialCostColumn())
        self.AddColumn(ProductTotalProductionTimeColumn())
        self.AddColumn(ProductFunctionBaseMarketPrice())
        self.AddColumn(ProductProductionCostPerProduct())
        self.AddColumn(ProductProfitPerDay())
