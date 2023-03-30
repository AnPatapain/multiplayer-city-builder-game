#include "game_packet_protocol.h"

#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>

game_packet* new_game_packet(uint8_t type){
    game_packet *new_packet = calloc(sizeof(game_packet), 1);
    if (new_packet == NULL) {
        return NULL;
    }
    new_packet->type = type;
    new_packet->reserved = 255;
    return new_packet;
}

int send_game_packet(game_packet *packet, int size_payload, int socket){
    int send_size = sizeof(game_packet) - sizeof(char*);
    int as_payload = 0;

    if (size_payload != 0 && packet->payload != NULL){
        send_size += size_payload;
        as_payload = 1;
    }

    char *send_bytes = calloc(1,send_size);
    if (memcpy(send_bytes,packet, sizeof(game_packet) - sizeof(char*)) == NULL) {
        return -1;
    }

    if (as_payload){
        if (memcpy(send_bytes, packet->payload, size_payload) == NULL){
            return -1;
        }
    }

    return send(socket,send_bytes,send_size,0);
}
