from class_types.buildind_types import BuildingTypes
from buildable.building import Buildings
from buildable.house import Houses

def building_constructor(building_type : BuildingTypes):
    match building_type:
        case BuildingTypes.SMALL_TENT:
            return Houses(5, (1, 1), 0, 0, 0, building_type)
        case BuildingTypes.LARGE_TENT:
            return Houses(28, (2, 2), 0, 0, 0, building_type)
        case BuildingTypes.SMALL_SHACK:
            return Houses(36, (2, 2), 0, 0, 0, building_type)
        case BuildingTypes.LARGE_SHACK:
            return Houses(44, (2, 2), 0, 0, 0, building_type)
        case BuildingTypes.SENATE:
            return Buildings(0,(1, 1), building_type)
        case BuildingTypes.ENGINEERS_POST:
            return Buildings(0, (1, 1), building_type)
        case BuildingTypes.PREFECTURE:
            return Buildings(0, (1, 1), building_type)
        case BuildingTypes.WELL:
            return Buildings(0, (1, 1), building_type)
        case BuildingTypes.FOUNTAIN:
            return Buildings(0, (1, 1), building_type)
        case BuildingTypes.BUILD_SIGN:
            return Buildings(0, (1, 1), building_type)
        case BuildingTypes.RUINS:
            return Buildings(0, (1, 1), building_type)
        case _:
            return None
