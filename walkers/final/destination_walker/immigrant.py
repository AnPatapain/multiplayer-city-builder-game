from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from map_element.tile import Tile
from walkers.destination_walker import DestinationWalker


class Immigrant(DestinationWalker):
    def __init__(self, associated_building: Buildable, dest: Tile, quantity: int):
        super().__init__(WalkerTypes.PREFET, associated_building)
        self.destination = dest
        self.quantity = quantity

    def spawn(self, tile: 'Tile'):
        super().spawn(tile)
        self.pathfinding()

    def destination_reached(self):
        self.associated_building.current_citizen += self.quantity
        self.associated_building.associated_walker = None
        self.delete()
