from abc import ABC
from typing import TYPE_CHECKING, Optional

from class_types.orientation_types import OrientationTypes
from game.game_controller import GameController
from game.textures import Textures

if TYPE_CHECKING:
    from buildable.buildable import Buildable
    from map_element.tile import Tile




class Walker(ABC):
    def __init__(self, walker_type, associated_building: 'Buildable', can_walk_outside_road: bool = False):
        self.walker_type = walker_type
        self.associated_building = associated_building
        self.can_walk_outside_road = can_walk_outside_road

        self.previous_tile: Optional[Tile] = None
        self.current_tile: Optional[Tile] = None
        self.next_tile: Optional[Tile] = None
        self.orientation = OrientationTypes.TOP_LEFT
        self.animation_frame = 1
        # goes from -10 to 10, to take 20 tick to navigate through a tile (also used for the offset
        self.walk_progression = -10


    def get_texture(self):
        return Textures.get_walker_texture(self.walker_type, self.orientation, self.animation_frame)

    def go_to_next_tile(self):
        if self.next_tile.get_road():
            self.current_tile.remove_walker(self)
            self.next_tile.add_walker(self)
            self.previous_tile = self.current_tile
            self.current_tile = self.next_tile
            self.next_tile = None
        else:
            self.next_tile = None
            self.previous_tile = self.current_tile

    def find_next_tile(self):
        print("FIXME: method find_next_tile not implemented!")
        pass

    def spawn(self, tile: 'Tile'):
        self.current_tile = tile
        self.current_tile.add_walker(self)
        GameController.get_instance().add_walker(self)
        self.find_next_tile()

    def delete(self):
        self.current_tile.remove_walker(self)
        self.associated_building.associated_walker = None
        GameController.get_instance().remove_walker(self)
        pass

    def destination_reached(self):
        pass

    def update(self):
        if self.walk_progression == 10:
            self.go_to_next_tile()
            self.walk_progression = -11

        self.walk_progression += 1
        # print("FIXME: method update not implemented!")
