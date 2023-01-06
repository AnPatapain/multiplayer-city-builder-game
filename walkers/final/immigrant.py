from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from map_element.tile import Tile
from walkers.walker import Walker


class Immigrant(Walker):
    def __init__(self, associated_building: Buildable, dest: Tile, quantity: int):
        super().__init__(WalkerTypes.MIGRANT, associated_building)
        self.destination = dest
        self.quantity = quantity

    def spawn(self, tile: 'Tile'):
        super().spawn(tile)
        self.navigate_to(self.associated_building.get_current_tile())
        self.next_tile = self.path_to_destination.pop(0)

    def destination_reached(self):
        self.associated_building.current_citizen += self.quantity
        self.delete()
