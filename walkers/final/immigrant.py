from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from map_element.tile import Tile
from walkers.walker import Walker
from game.id import ID_GEN


class Immigrant(Walker):
    def __init__(self, associated_building: Buildable, dest: Tile, quantity: int, player_id:int=0, id:int=0):
        super().__init__(WalkerTypes.MIGRANT, associated_building)
        self.destination = dest
        self.quantity = quantity
        id_create = ID_GEN()
        self.id = id_create.id_gen()

    def spawn(self, tile: 'Tile'):
        super().spawn(tile)
        self.navigate_to([self.associated_building.get_current_tile()])

    def destination_reached(self):
        self.associated_building.current_citizen += self.quantity
        self.delete()
