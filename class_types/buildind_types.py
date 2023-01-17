from enum import Enum

class BuildingTypes(Enum):
    VACANT_HOUSE = 1
    SMALL_TENT = 2
    LARGE_TENT = 3
    SMALL_SHACK = 4
    LARGE_SHACK = 5

    SENATE = 11
    ENGINEERS_POST = 12
    PREFECTURE = 13
    WELL = 20
    FOUNTAIN = 21
    HOSPITAL = 22
    SCHOOL = 23
    TEMPLE = 24
    THEATRE = 25

    BUILD_SIGN = 90
    RUINS = 91
    FIRE_RUINS = 92


    PELLE = 100 # i don't know the rule that we used to choose to number, I choose 100 but i don't know why i choose it : )
    ROCK = 101
    TREE = 102
    BIG_ROCK = 103

    GRANARY = 200
    WHEAT_FARM = 201
    MARKET = 202

    WHEAT_SOIL_LEVEL_1 = 203
    WHEAT_SOIL_LEVEL_2 = 204
    WHEAT_SOIL_LEVEL_3 = 205
    WHEAT_SOIL_LEVEL_4 = 205
    WHEAT_SOIL_LEVEL_5 = 205

    CERES = 206
    MARS = 207
    MERCURY = 208
    VENUS = 209
    NEPTUNE = 210
