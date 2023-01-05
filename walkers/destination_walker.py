from abc import ABC
from typing import TYPE_CHECKING, Optional

from walkers.walker import Walker

if TYPE_CHECKING:
    from buildable.buildable import Buildable
    from map_element.tile import Tile


class Cell:
    def __init__(self, score: int, tile: 'Tile'):
        self.score = score
        self.tile = tile
        self.previous: Optional['Cell'] = None
        self.depth = 10000000


class DestinationWalker(Walker, ABC):
    def __init__(self, walker_type, associated_building: 'Buildable', roads_only: bool = True):
        super().__init__(walker_type, associated_building)

        self.road_only = roads_only

        self.destination: Optional['Tile'] = None
        self.path_to_destination: list['Tile'] = []

    def find_next_tile(self):
        if self.current_tile == self.destination:
            self.destination_reached()

        if len(self.path_to_destination) > 0:
            # Get first element from path list
            return self.path_to_destination.pop(0)
        else:
            return self.current_tile

    def estimate_distance(self, src: 'Tile'):
        dest_x = abs(abs(src.x) - abs(self.destination.x))
        dest_y = abs(abs(src.y) - abs(self.destination.y))
        return dest_x + dest_y

    def pathfinding(self):
        open_set: list['Tile'] = [self.current_tile]
        came_from = {}
        g_score: dict['Tile', int] = {self.current_tile: 0}
        f_score: dict['Tile', int] = {self.current_tile: self.estimate_distance(self.current_tile)}

        while len(open_set) > 0:
            open_set.sort(key=lambda tile: f_score[tile])
            current = open_set.pop(0)

            if current == self.destination:
                self.path_to_destination.insert(0, current)
                while current in came_from:
                    current = came_from[current]
                    self.path_to_destination.insert(0, current)

                # reconstruct path
                self.path_to_destination.pop(0)
                self.next_tile = self.find_next_tile()

                return True

            for neighbor in current.get_adjacente_tiles():
                # Insert into array if not existing
                try:
                    temp = g_score[neighbor]
                except:
                    g_score[neighbor] = 1000000
                    f_score[neighbor] = 1000000

                if current.get_road() and neighbor.get_road():
                    tentative_gScore = g_score[current] + 1
                else:
                    tentative_gScore = g_score[current] + 100

                if tentative_gScore < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_gScore
                    f_score[neighbor] = tentative_gScore + self.estimate_distance(neighbor)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

        return False