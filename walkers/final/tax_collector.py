from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker


class TaxCollector(Walker):
    def __init__(self, associated_building: 'Buildable'):
        super().__init__(WalkerTypes.TAX_COLLECTOR, associated_building)



# class TaxCollector:
#     def __init__(self, city):
#         self.city = city
#         self.position = None

#     def collect_taxes(self):
#         # Check if the tax office is built
#         if not self.city.tax_office_built():
#             return

#         # Check if there are any citizens to collect taxes from
#         citizens = self.city.get_citizens_at(self.position)
#         if not citizens:
#             return

#         # Calculate the amount of taxes to collect based on population and tax rate
#         tax_rate = self.city.get_tax_rate()
#         population = self.city.get_population()
#         taxes_collected = int(population * tax_rate)

#         # Collect the taxes and add them to the city's treasury
#         self.city.collect_taxes(taxes_collected)

#     def move_to(self, position):
#         self.position = position

