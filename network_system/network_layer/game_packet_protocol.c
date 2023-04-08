#include "game_packet_protocol.h"

#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <errno.h>

static char *buffer;
static unsigned int buffer_size = 0;

static const uint32_t header_size = sizeof(game_packet) - sizeof(char*);

static int actual_event = 0;
static int player_id = 0;

void print_game_packet(const game_packet *packet){
#ifdef DEBUG
    printf("======== Packet %i ========\n", packet->id_event);
    printf("packet type: %i\n", packet->type);
    printf("Player_id: %i\n", packet->player_id);
    printf("Data Size: %i\n", packet->data_size);
    printf("====== End Packet %i ======\n", packet->id_event);
#endif
}

int new_payer_id(){
    srand(time(NULL));
    do {
        player_id = rand() % 65535;
    }while(player_id == 0);
    return player_id;
}

static void resize_buffer(const uint new_size){
    if (buffer_size){
        free(buffer);
    }
    buffer = calloc(1,new_size);
    buffer_size = new_size;
}

game_packet* new_game_packet(){
    game_packet *new_packet = calloc(sizeof(game_packet), 1);
    if (new_packet == NULL) {
        return NULL;
    }
    new_packet->reserved = 255;
    return new_packet;
}

void init_game_packet(game_packet *packet, const uint8_t type, const uint32_t size_payload){
    packet->type = type;
    actual_event += 1;
    packet->id_event = actual_event;
    packet->data_size = size_payload;
    packet->player_id = player_id;
}

int throw_new_packet(const uint8_t type, int socket){
    game_packet *message = new_game_packet();
    init_game_packet(message, type, 0);
    print_game_packet(message);
    if (send(socket,message,header_size,0) <= 0){
        return -1;
    }
    free(message);
    return 0;
}

int has_payload(const game_packet *packet){
    switch (packet->type) {
        case GPP_GAME_STATUS:
            return 1;
        case GPP_ALTER_GAME:
            return 1;
        case GPP_DELEGATE_ASK:
            return 1;
        case GPP_RESP_IP_LIST:
            return 1;
        case GPP_ASK_GAME_STATUS:
            return 1;
        default:
            return 0;
    }
}

int send_game_packet(const game_packet *send_packet, int socket){
    uint32_t send_size = header_size;
    int as_payload = 0;

    if (send_packet->data_size > 0 && send_packet->payload != NULL && has_payload(send_packet)){
        send_size += send_packet->data_size;
        as_payload = 1;
    }

    if (send_size > buffer_size){
        resize_buffer(send_size);
    }

    print_game_packet(send_packet);
    memset(buffer,'\0',buffer_size);
    if (memcpy(buffer,send_packet, sizeof(game_packet) - sizeof(char*)) == NULL) {
        return -1;
    }

    if (as_payload){
        if (memcpy(buffer + header_size, send_packet->payload, send_packet->data_size) == NULL){
            return -1;
        }
    }
    return (int) send(socket,buffer,send_size,0);
}

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

int is_valid(game_packet *packet){
    return (
            (GPP_CONNECT_NEW == packet->type
            || GPP_CONNECT_REQ == packet->type
            || GPP_CONNECT_OK == packet->type
            || GPP_ASK_GAME_STATUS == packet->type
            || GPP_GAME_STATUS == packet->type
            || GPP_ALTER_GAME == packet->type
            || GPP_DELEGATE_ASK == packet->type
            || GPP_DELEGATE_OK == packet->type
            || GPP_ASK_IP_LIST == packet->type
            || GPP_RESP_IP_LIST == packet->type
            || GPP_BAD_IDENT == packet->type)
            && packet->reserved == 255
    );

}

int receive_game_packet(game_packet *recv_packet, int socket){

    int recep = (int) recv(socket,recv_packet,header_size,0);
    if (recep == 0){
        return 0;
    }
    if (recep < header_size || !is_valid(recv_packet)){
        return -1;
    }

    if (recv_packet->data_size > 0 && has_payload(recv_packet)){
        recv_packet->payload = calloc(recv_packet->data_size,1);
        recep += (int) recv(socket,recv_packet->payload,recv_packet->data_size,MSG_WAITALL);

    }
    flush_socket(socket);
    return recep;
}

game_packet *encapsulate_object_packets(const Object_packet *object, int nb_object, uint8_t type){

    if (object == NULL){
        return NULL;
    }
    uint size_all = 0;
    const uint object_size = get_object_size();
    for (int i = 0; i < nb_object; i++){
        size_all += object_size;
        size_all += object[i].object_size;
    }

    game_packet *new_packet = new_game_packet();
    init_game_packet(new_packet,type,size_all);

    new_packet->payload = calloc(size_all,1);

    int cursor = 0;
    for (int i = 0; i < nb_object; i++){

        memcpy(new_packet->payload + cursor,object + i,object_size);
        cursor += (int) object_size;

        if (object[i].object_size > 0){
            memcpy(new_packet->payload + cursor,object[i].data,object[i].object_size);
            cursor += (int) object[i].object_size;
        }
    }
    return new_packet;
}

Object_packet *uncap_object_packets(int *nb_packet, const game_packet *packet){
    if (nb_packet == NULL){
        return NULL;
    }
    const int size = (int) packet->data_size;

    *nb_packet = 0;
    uint cursor = 0;
    Object_packet *current_object;
    const uint object_size = get_object_size();
    while (cursor < size){
        current_object = (Object_packet*) (packet->payload + cursor);
        (*nb_packet)++;
        if (current_object->object_size > 0){
            cursor += current_object->object_size;
        }
        cursor += object_size;
    }

    Object_packet *obj_tab = calloc(sizeof(Object_packet),*nb_packet);
    cursor = 0;
    for (int i = 0; i < *nb_packet; i++){
        memcpy(obj_tab + i, packet->payload + cursor, object_size);
        cursor += object_size;
        if (obj_tab[i].object_size > 0){
            obj_tab[i].data = calloc(obj_tab[i].object_size,1);
            memcpy(obj_tab[i].data,packet->payload + cursor,obj_tab[i].object_size);
            cursor += obj_tab[i].object_size;
        }
    }
    return obj_tab;
}


int get_player_id(){
    return player_id;
}