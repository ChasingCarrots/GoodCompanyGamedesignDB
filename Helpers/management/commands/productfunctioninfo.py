from django.core.management.base import BaseCommand, CommandError
from Production.models import *

class Command(BaseCommand):
    help = 'Outputs information concerning ProductFunctions'

    def add_arguments(self, parser):
        parser.add_argument('--functionid', type=int, help="(optional) only output for the ProductFunction with that id.")

    def handle(self, *args, **options):
        if options["functionid"]:
            function = ProductFunction.objects.get(id=options["functionid"])
            self.handleProductfunction(function)
        else:
            for function in ProductFunction.objects.all():
                self.handleProductfunction(function)

    def handleProductfunction(self, function):
        self.stdout.write("Function %s" % function)
        # first we create queries to simply filter out all the modules
        # that don't satisfy the requirements (one query per requirement)
        modulesForRequirements = []
        for requirement in ProductFunctionFeatureRequirement.objects.filter(Function=function):
            if requirement.Feature.Type == common.MAXIMUM:
                modulesForRequirements.append((requirement,
                    ModuleFeature.objects.filter(ProductFeature=requirement.Feature,
                                                FeatureValue__gte=requirement.FeatureValue)))
            elif requirement.Feature.Type == common.MINIMUM:
                modulesForRequirements.append((requirement,
                    ModuleFeature.objects.filter(ProductFeature=requirement.Feature,
                                                 FeatureValue__lte=requirement.FeatureValue)))
            else:
                modulesForRequirements.append((requirement,
                    ModuleFeature.objects.filter(ProductFeature=requirement.Feature,
                                                 FeatureValue=requirement.FeatureValue)))

        # every viable product type has to be handled independently!
        for productType in function.ViableProductTypes.all():
            self.stdout.write("   ProductType %s" % productType)
            for requirement,moduleQuery in modulesForRequirements:
                # we can filter the query further to the possible slot types
                productTypeModuleQuery = moduleQuery.filter(Module__FitsIntoSlot__in=productType.Slots.all())
                self.stdout.write("      Requirement %d %s (id:%d) has %d possible modules" %
                                  (requirement.FeatureValue, requirement.Feature.Name, requirement.Feature.id, productTypeModuleQuery.count()))
