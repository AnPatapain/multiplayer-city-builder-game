from enum import IntEnum

# IntEnum: 1000 - 1999 range

class BuildingTypes(IntEnum):
    VACANT_HOUSE = 1001
    SMALL_TENT = 1002
    LARGE_TENT = 1003
    SMALL_SHACK = 1004
    LARGE_SHACK = 1005

    SENATE = 1011
    ENGINEERS_POST = 1012
    PREFECTURE = 1013
    WELL = 1020
    FOUNTAIN = 1021
    HOSPITAL = 1022
    SCHOOL = 1023
    TEMPLE = 1024
    THEATRE = 1025

    BUILD_SIGN = 1090
    RUINS = 1091
    FIRE_RUINS = 1092
    ENTRY_FLAG = 1093
    LEAVE_FLAG = 1094

    PELLE = 1100 # i don't know the rule that we used to choose to number, I choose 100 but i don't know why i choose it : )
    ROCK = 1101
    TREE = 1102
    BIG_ROCK = 1103

    GRANARY = 1200
    WHEAT_FARM = 1201
    MARKET = 1202


    CERES = 1206
    MARS = 1207
    MERCURY = 1208
    VENUS = 1209
    NEPTUNE = 1210
