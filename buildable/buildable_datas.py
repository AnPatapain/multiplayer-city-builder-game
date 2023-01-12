from enum import Enum

from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes

buildable_cost: dict[Enum, int] = {
    BuildingTypes.VACANT_HOUSE: 10,
    BuildingTypes.SMALL_TENT: 10,
    BuildingTypes.LARGE_TENT: 100,
    BuildingTypes.SMALL_SHACK: 500,
    BuildingTypes.LARGE_SHACK: 1000,
    BuildingTypes.PREFECTURE: 30,
    BuildingTypes.ENGINEERS_POST: 30,
    BuildingTypes.WELL: 20,
    BuildingTypes.WHEAT_FARM: 40,
    BuildingTypes.GRANARY: 100,
    BuildingTypes.MARKET: 40,
    BuildingTypes.PELLE: 2,
    RoadTypes.TL_TO_BR: 4,
    BuildingTypes.HOSPITAL: 300,
    BuildingTypes.SENATE: 400,
    BuildingTypes.SCHOOL: 50,
    BuildingTypes.TEMPLE: 50,
    BuildingTypes.THEATRE: 50,

}

buildable_size: dict[BuildingTypes | RoadTypes, tuple[int, int]] = {
    BuildingTypes.TREE: (1, 1),
    BuildingTypes.ROCK: (1, 1),
    BuildingTypes.BIG_ROCK: (2, 2),
    BuildingTypes.VACANT_HOUSE: (1, 1),
    BuildingTypes.SMALL_TENT: (1, 1),
    BuildingTypes.LARGE_TENT: (1, 1),
    BuildingTypes.SMALL_SHACK: (1, 1),
    BuildingTypes.LARGE_SHACK: (1, 1),
    BuildingTypes.PREFECTURE: (1, 1),
    BuildingTypes.ENGINEERS_POST: (1, 1),
    BuildingTypes.WELL: (1, 1),
    BuildingTypes.WHEAT_FARM: (3, 3),
    BuildingTypes.GRANARY: (3, 3),
    BuildingTypes.MARKET: (2, 2),
    BuildingTypes.HOSPITAL: (3, 3),
    BuildingTypes.SENATE: (5, 5),
    BuildingTypes.SCHOOL: (3, 3),
    BuildingTypes.TEMPLE: (2, 2),
    BuildingTypes.THEATRE: (3, 3),
    BuildingTypes.PELLE: (1, 1),
    BuildingTypes.RUINS: (1, 1),
    BuildingTypes.FIRE_RUINS: (1, 1),
    RoadTypes.TL_TO_BR: (1, 1),
    BuildingTypes.ENTRY_FLAG: (1, 1),
    BuildingTypes.LEAVE_FLAG: (1, 1),
}
