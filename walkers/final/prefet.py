from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from walkers.walker import Walker


class Prefet(Walker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.PREFET, associated_building, max_walk_distance=10, roads_only=True)
