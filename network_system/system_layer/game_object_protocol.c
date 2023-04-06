#include "Message.h"
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <errno.h>

char *buffer;
unsigned int buffer_size = 0;

const uint32_t header_size = sizeof(Object_packet) - sizeof(char*);

void flush_socket(int socket){
    int recept;
    char buf[1024];
    do{
        recept = (int) recv(socket,buf,1024,MSG_DONTWAIT);
        if (recept == -1 && errno == EAGAIN){
            return;
        }
    }while(recept >= 1024);
}

int has_data(Object_packet *packet){
    switch (packet->object_type.typeObject){
        case C_COMMAND:
            return 0;
        default:
            return 1;
    }
}

int receive_object_packet(Object_packet *recv_packet, int system_socket){
    int recep = (int) recv(system_socket,recv_packet,header_size,0);
    if (recep == 0){
        return 0;
    }
    if (recv_packet->object_size > 0 && has_data(recv_packet1)){
        recv_packet->data = calloc(recv_packet->object_size,1);
        recep += (int) recv(system_socket,recv_packet->data,recv_packet->object_size,MSG_WAITALL);

    }
    flush_socket(system_socket);
    return recep;
}