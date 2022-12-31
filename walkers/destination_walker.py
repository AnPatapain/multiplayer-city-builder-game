from abc import ABC

from buildable.buildable import Buildable
from walkers.walker import Walker


class DestinationWalker(Walker, ABC):
    def __init__(self, walker_type, associated_building: Buildable):
        super().__init__(walker_type, associated_building)
