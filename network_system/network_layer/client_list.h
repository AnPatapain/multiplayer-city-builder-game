#ifndef CLIENT_LIST
#define CLIENT_LIST

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdint.h>
#include <stdlib.h>

#include "game_packet_protocol.h"

typedef enum {FALSE = 0, TRUE = 1} bool;

struct client_game
{
    int socket_client;
    uint16_t player_id;
    struct sockaddr_in sockaddr_client;
    bool as_initial;
    struct client_game* next;
};

typedef struct client_game client_game;


client_game *first_client();
bool id_exist(client_game *client_to_check,uint16_t id);
int cgl_append(client_game* new_client);
int clg_remove(client_game* client_to_delete);
game_ip *get_all_ips(int *nb_client, const client_game *req_client);

/**
 * @param: fd_server: fd to set al client
 * @return: Fd max
*/
void cgl_set_all_client(fd_set *fd_server, int *max_fd);

#endif //CLIENT_LIST