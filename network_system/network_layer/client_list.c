#include "client_list.h"

#include <sys/select.h>

client_game *list_client = NULL;

int cgl_set_all_client(fd_set *fd_server){
    client_game *client = list_client;
    int max_fd = 0;
    while (client != NULL){
        if (client->socket_client > max_fd){
            max_fd = client->socket_client;
        }

        FD_SET(client->socket_client,fd_server);
        client = client->next;
    }
    return max_fd;
}

client_game *last_client(){
    if (list_client == NULL){
        return NULL;
    }
    client_game *last = list_client;
    while (list_client->next != NULL) {
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
    return 0;
}