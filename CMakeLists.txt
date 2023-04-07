cmake_minimum_required(VERSION 3.24)
project(taboule_raza C)

set(CMAKE_C_STANDARD 11)

include_directories(network_system/network_layer)
include_directories(network_system/system_layer)

add_executable(taboule_raza
        network_system/network_layer/client_list.c
        network_system/network_layer/client_list.h
        network_system/network_layer/game_packet_protocol.h
        network_system/network_layer/game_packet_protocol.c
        network_system/network_layer/game_server.c
        network_system/network_layer/game_server.h
        network_system/network_layer/message_type.h
        network_system/system_layer/game_object_protocol.h network_system/system_layer/game_object_protocol.c)
