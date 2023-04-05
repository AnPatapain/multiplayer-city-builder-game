#include "client_list.h"

#include <sys/select.h>
#include <netinet/in.h>

client_game *list_client = NULL;
uint number_client = 0;

client_game *first_client(){
    return list_client;
}

bool id_exist(client_game *client_to_check,uint16_t id){
    if (id == 0 || id == 65535){
        return TRUE;
    }
    client_game *client = list_client;
    while (client != NULL){
        if (client->player_id == id && client != client_to_check){
            return TRUE;
        }
        client = client->next;
    }
    return FALSE;
}

void cgl_set_all_client(fd_set *fd_server, int *max_fd) {
    client_game *client = list_client;
    while (client != NULL){
        if (client->socket_client > *max_fd){
            *max_fd = client->socket_client;
        }

        FD_SET(client->socket_client,fd_server);
        client = client->next;
    }
}

client_game *last_client(){
    if (list_client == NULL){
        return NULL;
    }
    client_game *last = list_client;
    while (last->next != NULL) {
        last = last->next;
    }
    return last;
}

int cgl_append(client_game* new_client){
    if (new_client == NULL) {
        return -1;
    }

    if (list_client){
        client_game* last = last_client();
        last->next = new_client;
    }
    else{
        list_client = new_client;
    }
    number_client++;
    new_client->next=NULL;
    return 0;
}

game_ip *get_all_ips(int *nb_client, const client_game *req_client) {
    game_ip *ips = calloc(number_client, sizeof(uint32_t));
    client_game *client = list_client;
    int i = 0;
    while (client != NULL){
        if (client == req_client){
            client = client->next;
            continue;
        }
        ips[i] = client->sockaddr_client.sin_addr.s_addr;
        i++;
        client = client->next;
    }
    *nb_client = i;
    return ips;
}