#ifndef GOP_H
#define GOP_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>

#include "object_type.h"

#define C_COMMAND 65535


struct Object_packet {
    uint16_t id_player;
    uint16_t command;
    uint32_t object_size;
    uint32_t id_object;
    char *data;
};
typedef struct Object_packet Object_packet;

Object_packet* new_object_packet();
void init_object_packet(Object_packet *packet, uint16_t command, uint32_t size_data);
int throw_new_object(uint16_t command, int system_socket);
int is_for_C(Object_packet *packet);
void print_object_packet(const Object_packet *packet);
int send_object_packet(Object_packet *send_packet, int system_socket);
int receive_object_packet(Object_packet *recv_packet, int system_socket);
uint32_t get_object_size();

#endif // GOP_H