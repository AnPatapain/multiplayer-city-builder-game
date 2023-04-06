import random
from abc import ABC
from typing import TYPE_CHECKING, Optional
from game.id import ID_GEN
from class_types.orientation_types import OrientationTypes
from game.game_controller import GameController
from game.textures import Textures

if TYPE_CHECKING:
    from buildable.buildable import Buildable
    from class_types.walker_types import WalkerTypes
    from map_element.tile import Tile


class Walker(ABC):
    def __init__(self, walker_type, associated_building: 'Buildable', roads_only: bool = False,
                 max_walk_distance: int = -1, player_id :int=0, id : int= 0):
        self.walker_type: 'WalkerTypes' = walker_type
        self.associated_building: 'Buildable' = associated_building

        self.previous_tile: Optional[Tile] = None
        self.current_tile: Optional[Tile] = None
        self.next_tile: Optional[Tile] = None

        self.destination: Optional['Tile'] = None
        self.path_to_destination: list['Tile'] = []

        self.roads_only = roads_only
        self.orientation_from_previous_tile = OrientationTypes.TOP_LEFT
        self.orientation_to_next_tile = OrientationTypes.TOP_LEFT
        self.animation_frame = 1

        self.walk_distance = 0
        self.max_walk_distance = max_walk_distance
        # goes from -14 to 14, to take 28 tick to navigate through a tile (also used for the offset
        self.walk_progression = -14

        id_create = ID_GEN()
        self.id = id_create.id_gen()

    def get_texture(self):
        if self.walk_progression < 0:
            return Textures.get_walker_texture(self.walker_type, self.orientation_from_previous_tile, int(self.animation_frame))
        else:
            return Textures.get_walker_texture(self.walker_type, self.orientation_to_next_tile, int(self.animation_frame))

    def go_to_next_tile(self):
        # If max_walk_distance was set we must check if the current walk distance reach it or not if it does navigate the walker to its building
        if self.max_walk_distance != -1:
            if len(self.path_to_destination) == 0:
                self.walk_distance += 1

        if self.next_tile:
            self.current_tile.remove_walker(self)
            self.next_tile.add_walker(self)
            self.previous_tile = self.current_tile
            self.current_tile = self.next_tile
            self.next_tile = None
        else:
            self.next_tile = None
            self.previous_tile = self.current_tile

        self.next_tile = self.find_next_tile()
        self.update_direction()

    def on_walk_distance_reached(self):
        pass

    def find_next_tile(self) -> 'Tile':
        if self.current_tile == self.destination:
            self.destination_reached()

        # Directly follow the path if present
        if len(self.path_to_destination) > 0:
            # Get first element from path list
            return self.path_to_destination.pop(0)

        # Else find an adjacent road to follow automatically
        candidates = self.current_tile.get_adjacente_tiles()
        candidates = list(
            filter(lambda candidate: candidate is not self.previous_tile and candidate.get_road() is not None,
                   candidates))

        if len(candidates) == 0:
            if self.previous_tile:
                candidates.append(self.previous_tile)
            else:
                candidates.append(self.current_tile)

        return random.choice(candidates)

    def update_direction(self):
        self.orientation_from_previous_tile = self.orientation_to_next_tile

        # x = col, y = row
        if self.next_tile.y < self.current_tile.y:
            self.orientation_to_next_tile = OrientationTypes.TOP_LEFT
        elif self.next_tile.x < self.current_tile.x:
            self.orientation_to_next_tile = OrientationTypes.TOP_RIGHT
        elif self.next_tile.y > self.current_tile.y:
            self.orientation_to_next_tile = OrientationTypes.BOTTOM_RIGHT
        elif self.next_tile.x > self.current_tile.x:
            self.orientation_to_next_tile = OrientationTypes.BOTTOM_LEFT


    def spawn(self, tile: 'Tile'):
        self.current_tile = tile
        self.current_tile.add_walker(self)
        GameController.get_instance().add_walker(self)
        self.next_tile = self.find_next_tile()
        self.update_direction()

    def delete(self):
        self.current_tile.remove_walker(self)
        self.associated_building.associated_walker = None
        GameController.get_instance().remove_walker(self)
        pass

    def destination_reached(self):
        self.delete()

    def update(self):
        if self.walk_progression == 14:
            self.go_to_next_tile()
            self.walk_progression = -15

        if self.walk_progression == 0 and self.walk_distance != -1:
            if self.walk_distance == self.max_walk_distance:
                self.on_walk_distance_reached()
                self.walk_distance = -1
                res = self.navigate_to(self.associated_building.get_all_building_tiles())
                if not res:
                    self.delete()
                    return

        self.animation_frame += 0.3
        self.walk_progression += 1

    def navigate_to(self, dest: list['Tile']):
        path = self.current_tile.find_path_to(dest, roads_only=self.roads_only)
        if not path:
            return False
        else:
            self.destination = path[-1]
            self.path_to_destination = path
            self.path_to_destination.pop(0)
            self.next_tile = self.path_to_destination.pop(0)
            self.previous_tile = self.current_tile
            self.update_direction()

            return True
