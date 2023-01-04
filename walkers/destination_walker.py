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

    def pathfinding(self, roads_only: bool = True) -> bool:
        open_list: set[Cell] = set()
        closed_list: set[Cell] = set()

        open_list.add(Cell(1, self.current_tile))

        while len(open_list) > 0:
            current = open_list.pop()
            closed_list.add(current)

            if current.tile == self.destination:
                print("Path found")
                while current and current.tile:
                    self.path_to_destination.insert(0, current.tile)
                    current = current.previous
                # Next tile is already set to the current tile
                self.path_to_destination.pop(0)
                self.next_tile = self.find_next_tile()
                return True

            neighbors = current.tile.get_adjacente_tiles()

            # remove neighbors that are already closed
            for closed in closed_list:
                if closed.tile in neighbors:
                    neighbors.remove(closed.tile)

            for neighbor in neighbors:
                neighbor_cell = None
                for opened in open_list:
                    if opened.tile == neighbor:
                        neighbor_cell = opened
                        break

                if neighbor_cell:
                    if current.depth < neighbor_cell.depth:
                        neighbor_cell.previous = current
                        neighbor_cell.score = current.score+1

                else:
                    c = Cell(current.score+1, neighbor)
                    c.previous = current
                    c.depth = current.depth+1
                    open_list.add(c)

        return False
