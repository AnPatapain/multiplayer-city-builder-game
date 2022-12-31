from buildable.buildable import Buildable
from class_types.walker_types import WalkerTypes
from walkers.random_walker import RandomWalker


class Prefet(RandomWalker):
    def __init__(self, associated_building: Buildable):
        super().__init__(WalkerTypes.PREFET, associated_building, 45)
