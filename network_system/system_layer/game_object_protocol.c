#include "game_object_protocol.h"
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <errno.h>

#include "../network_layer/game_packet_protocol.h"

static char *buffer;
static unsigned int buffer_size = 0;

static const uint32_t header_size = 12;

void print_object_packet(const Object_packet *packet){
#ifdef DEBUG
    printf("======== Object %i ========\n", packet->id_object);
    printf("command: %i\n", packet->command);
    printf("Player_id: %i\n", packet->id_player);
    printf("Data Size: %i\n", packet->object_size);
    printf("====== End Packet %i ======\n", packet->id_object);
#endif
}

Object_packet* new_object_packet(){
    Object_packet *new_packet = calloc(sizeof(Object_packet), 1);
    if (new_packet == NULL) {
        return NULL;
    }
    //new_packet->reserved = 4294967295;
    return new_packet;
}


void init_object_packet(Object_packet *packet, const uint16_t command, const uint32_t size_data){
    packet->object_size = size_data;
    packet->command = command;
    packet->id_player = get_player_id();
}

int is_for_C(Object_packet *packet){
    return (packet->command == C_COMMAND);
}

int has_data(Object_packet *packet){
    switch (packet->command){
        case C_COMMAND:
            return 0;
        default:
            return 1;
    }
}

static void resize_buffer(const uint new_size){
    if (buffer_size){
        free(buffer);
    }
    buffer = calloc(1,new_size);
    buffer_size = new_size;
}

int send_object_packet(Object_packet *send_packet, int system_socket){
    uint32_t send_size = header_size;
    int as_payload = 0;

    if (send_packet->object_size > 0 && send_packet->data != NULL && has_data(send_packet)){
        send_size += send_packet->object_size;
        as_payload = 1;
    }

    if (send_size > buffer_size){
        resize_buffer(send_size);
    }

    memset(buffer,'\0',buffer_size);
    if (memcpy(buffer,send_packet, header_size) == NULL) {
        return -1;
    }

    if (as_payload){
        if (memcpy(buffer + header_size, send_packet->data, send_packet->object_size) == NULL){
            return -1;
        }
    }
    return (int) send(system_socket,buffer,send_size,0);
}

int receive_object_packet(Object_packet *recv_packet, int system_socket){
    int recep = (int) recv(system_socket,recv_packet,header_size,0);
    if (recep == 0){
        return 0;
    }
    if (recv_packet->object_size > 0 && has_data(recv_packet)){
        recv_packet->data = calloc(recv_packet->object_size,1);
        recep += (int) recv(system_socket,recv_packet->data,recv_packet->object_size,MSG_WAITALL);

    }
    flush_socket(system_socket);
    return recep;
}

uint32_t get_object_size(){
    return header_size;
}