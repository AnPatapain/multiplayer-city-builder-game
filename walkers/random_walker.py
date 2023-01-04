import random
from abc import ABC
from typing import TYPE_CHECKING

from walkers.walker import Walker

if TYPE_CHECKING:
    from map_element.tile import Tile
    from buildable.buildable import Buildable


class RandomWalker(Walker, ABC):
    def __init__(self, walker_type, associated_building: 'Buildable', max_walk_distance: int):
        super().__init__(walker_type, associated_building)

        self.max_walk_distance = max_walk_distance
        self.current_walk_distance = 0

    def find_next_tile(self) -> 'Tile':
        candidates = self.current_tile.get_adjacente_tiles()
        candidates = list(filter(lambda candidate: candidate is not self.previous_tile and candidate.get_road() is not None, candidates))

        if len(candidates) == 0:
            if self.previous_tile:
                candidates.append(self.previous_tile)
            else:
                candidates.append(self.current_tile)

        return random.choice(candidates)
