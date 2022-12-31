import random
from abc import ABC

from buildable.buildable import Buildable
from game.gameController import GameController
from walkers.walker import Walker


class RandomWalker(Walker, ABC):
    def __init__(self, walker_type, associated_building: Buildable, max_walk_distance: int):
        super().__init__(walker_type, associated_building)

        self.max_walk_distance = max_walk_distance
        self.current_walk_distance = 0


    def update(self):
        if self.walk_progression == 10:
            self.go_to_next_tile()
            self.find_next_tile()
            self.walk_progression = -11

        self.walk_progression += 1

    def find_next_tile(self):
        map = GameController.get_instance().get_map()

        found_tiles = []

        if self.current_tile.x >= 1:
            tile = map[self.current_tile.x-1][self.current_tile.y]
            if tile.get_road() and tile is not self.previous_tile:
                found_tiles.append(tile)

        if self.current_tile.x < 50:
            tile = map[self.current_tile.x+1][self.current_tile.y]
            if tile.get_road() and tile is not self.previous_tile:
                found_tiles.append(tile)

        if self.current_tile.y < 50:
            tile = map[self.current_tile.x][self.current_tile.y+1]
            if tile.get_road() and tile is not self.previous_tile:
                found_tiles.append(tile)

        if self.current_tile.y >= 1:
            tile = map[self.current_tile.x][self.current_tile.y-1]
            if tile.get_road() and tile is not self.previous_tile:
                found_tiles.append(tile)

        if len(found_tiles) == 0:
            if self.previous_tile:
                found_tiles.append(self.previous_tile)
            else:
                found_tiles.append(self.current_tile)

        self.next_tile = random.choice(found_tiles)
