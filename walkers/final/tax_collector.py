from typing import TYPE_CHECKING
from walkers.walker import Walker
from class_types.walker_types import WalkerTypes
from buildable.house import House
from game.game_controller import GameController

if TYPE_CHECKING:
    from buildable.structure import Structure
    from buildable.buildable import Buildable
    


class TaxCollector(Walker):

    def __init__(self, associated_building: 'Buildable'):
        super().__init__(WalkerTypes.TAX_COLLECTOR, associated_building, max_walk_distance=10, roads_only=True)

        self.tax = 0

    def update(self):

        super().update()
        tiles = self.current_tile.get_adjacente_tiles(2)

        # Collect taxes

        for tile in tiles:
            if tile.get_building():
                building = tile.get_building()
                print("this is a building")
                if isinstance(building, House) and building.get_has_taxes():
                    print("this is a house")
                    building.set_has_taxes(False)
                    self.tax += building.tax


    def destination_reached(self):
        print(self.tax)
        GC = GameController.get_instance()
        GC.denier += self.tax
        super().destination_reached()






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

