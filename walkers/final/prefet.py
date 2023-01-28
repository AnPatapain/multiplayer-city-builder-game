from enum import Enum
from typing import Optional

from buildable.buildable import Buildable
from buildable.final.buildable.ruin import Ruin
from buildable.house import House
from buildable.structure import Structure
from class_types.orientation_types import OrientationTypes
from class_types.walker_types import WalkerTypes
from game.textures import Textures
from walkers.walker import Walker

class State(Enum):
    PATROL = 1
    BACK_TO_BUILDING = 2
    GO_TO_FIRE = 3
    EXTINGUISH_FIRE = 4


class Prefet(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.PREFET, associated_building, max_walk_distance=10, roads_only=True)
        self.state = State.PATROL
        self.building_being_extinguished: Optional['Buildable'] = None
        self.extinguish_progress = 0

    def update(self):
        super().update()
        tiles = self.current_tile.get_adjacente_tiles(2)
        if self.state == State.EXTINGUISH_FIRE:
            self.walk_progression = 0
            self.extinguish_progress += 1
            if self.extinguish_progress == 100:
                self.building_being_extinguished.is_on_fire = False

                self.extinguish_progress = 0
                self.state = State.PATROL
                self.building_being_extinguished = None

        for tile in tiles:
            build = tile.get_building()
            if build:
                if isinstance(build, House) or isinstance(build, Structure) or isinstance(build, Ruin):
                    build.risk.reset_fire_risk()
                    if build.is_on_fire and self.state == State.PATROL:
                        self.state = State.GO_TO_FIRE
                        self.building_being_extinguished = build
                        self.roads_only = False
                        self.navigate_to(build.get_all_building_tiles())
                        self.roads_only = True


                        # We don't want to walk on the building, only in front of it. It allows the walker to go back on the road easily
                        if len(self.path_to_destination) >= 2:
                            self.path_to_destination.pop()
                            self.destination = self.path_to_destination[-1]

    def on_walk_distance_reached(self):
        self.state = State.BACK_TO_BUILDING

    def destination_reached(self):
        if self.state == State.GO_TO_FIRE:
            self.state = State.EXTINGUISH_FIRE


        elif self.state == State.BACK_TO_BUILDING:
            self.delete()

    def get_texture(self):
        if self.state == State.EXTINGUISH_FIRE:
            return Textures.get_walker_texture(WalkerTypes.PREFET_EXTINGUISHING_FIRE, OrientationTypes.BOTTOM_RIGHT, int(self.animation_frame))
        else:
            return super().get_texture()
