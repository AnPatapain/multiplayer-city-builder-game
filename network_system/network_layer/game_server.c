#include "game_server.h"



client_game* add_client(int socket_client){
    client_game* new_client = calloc(1,sizeof(client_game));
    
    if (new_client == NULL){
        perror("Calloc");
        return NULL;
    }
    new_client->player_id = 0;
    new_client->socket_client = socket_client;
    new_client->as_init = TRUE;
    
    if (cgl_append(new_client) < 0){
        return NULL;
    }
    return new_client;
}

int new_connection(client_game *client,game_packet *packet){
    if (id_exist(client, packet->player_id)){
        if (throw_new_packet(GPP_BAD_IDENT,client->socket_client) < 0){
            return -1;
        }
        return 0;
    }
    return req_connection(client,packet);
}

int req_connection(client_game *client,game_packet *packet){
    client->player_id = packet->player_id;
    if (throw_new_packet(GPP_CONNECT_OK,client->socket_client) < 0){
        return -1;
    }
    return 0;
}

int get_ip_list(client_game *client, game_packet *packet){
    game_packet *ip_list_packet = new_game_packet();
    int number_ip;
    game_ip *ips = get_all_ips(&number_ip);
    int size_payload = number_ip * sizeof(uint32_t);

    init(ip_list_packet,GPP_RESP_IP_LIST,size_payload);
    ip_list_packet->payload = (char *) ips;

    if (send_game_packet(packet,client->socket_client) <= 0){
        return -1;
    }
    free(ip_list_packet);
    free(ips);
    return 0;
}

int type_check(client_game *client,game_packet *packet){
    switch (packet->type) {
        case GPP_CONNECT_NEW:
            return new_connection(client,packet);
        case GPP_CONNECT_REQ:
            return req_connection(client,packet);
        case GPP_CONNECT_OK:
            client->player_id = packet->player_id;
            return 0;
        case GPP_ASK_GAME_STATUS:
            //TODO: Request python for all game
            break;
        case GPP_GAME_STATUS:
            //TODO: Send data to python
            break;
        case GPP_ALTER_GAME:
            //TODO: Send data to python
            break;
        case GPP_DELEGATE_ASK:
            //TODO: Notify python to take own of this data
            break;
        case GPP_DELEGATE_OK:
            //TODO: Python take data
            break;
        case GPP_ASK_IP_LIST:
            return get_ip_list(client,packet);
        case GPP_RESP_IP_LIST:
            //TODO: Mange reception of game IP list
            break;
        case GPP_BAD_IDENT:
            //TODO: (implement bad request + log)?
            break;
        default:
            //TODO: (implement bad request + log)?
            break;
    }
}

int check_all_client(fd_set *fds){
    client_game *client = first_client();
    game_packet *recv_packet = new_game_packet();
    while (client != NULL){
        if (FD_ISSET(client->socket_client, fds)){

            if (receive_game_packet(recv_packet,client->socket_client) == 0){
                //TODO: disconnect
            }
            //TODO: type check
        }
    }
    free(recv_packet);
    return 0;
}

int game_server(int socket) {
    fd_set fd_listen_sock;
    int number_fd;
    int max_fd = socket;
    
    while (1){
        FD_ZERO(&fd_listen_sock);
        FD_SET(socket,&fd_listen_sock);
        
        number_fd = select(cgl_set_all_client(&fd_listen_sock) +1, &fd_listen_sock,NULL,NULL,NULL);

        if (number_fd < 0){
            perror("select :");
            return -1;
        }

        if (FD_ISSET(socket,&fd_listen_sock)){
            if (add_client(socket) == NULL){
                return -1;
            }
            printf("LOG: new client_game accept\n");
        }


    }
}

int init_connection_existant_game(char *ip_address){

    // Create new socket
    struct sockaddr_in sock_adresse = {0};
    sock_adresse.sin_port = htons(PORT);

    if (inet_aton(ip_address,&(sock_adresse.sin_addr)) == 0){
        printf("Erreur : inet_aton\n");
    }

    int new_socket = socket(AF_INET, SOCK_STREAM, 6);
    if (new_socket < 0){
        perror("socket()");
        close(new_socket);
        return -1;
    }

    if (connect(new_socket, (struct sockaddr *) &sock_adresse, sizeof(sock_adresse)) == -1){
        perror("Connect");
        close(new_socket);
        return -1;
    }

    client_game* new_connection = add_client(new_socket);
    if ( new_connection == NULL){
        return -1;
    }
    new_connection -> as_init = FALSE;

    game_packet *connection = new_game_packet();
    init(connection,GPP_CONNECT_NEW,0);

    if (connection == NULL){
        return -1;
    }
    connection->payload = NULL;

    // Start protocol connection
    if (send_game_packet(connection,new_socket) < 1){
        printf("send game packet protocol failed");
        return -1;
    }

    struct timeval timeout = {0};
    fd_set fd_set_connect;

    do {
        timeout.tv_sec = TIMEOUT;

        FD_ZERO(&fd_set_connect);
        FD_SET(new_socket, &fd_set_connect);
        select(new_socket + 1, &fd_set_connect, NULL, NULL, &timeout);

        if (!FD_ISSET(new_socket, &fd_set_connect)) {
            printf("Error can't connect to game");
            close(new_socket);
            return 1;
        }

        if (receive_game_packet(connection, new_socket) == 0) {
            return 1;
        }

    }while (connection->type == GPP_BAD_IDENT);

    if (connection->type != GPP_CONNECT_OK){
        printf("Error bad connection type");
        close(new_socket);
        return -1;
    }

    // Add client to list
    client_game *new_client = add_client(new_socket);
    new_client->player_id = connection->player_id;
    printf("Event: %i: Connected to client %i",connection->id_event,new_client->player_id);

    // Ask for ip
    init(connection,GPP_ASK_IP_LIST,0);
    if (send_game_packet(connection,new_client->socket_client) < 1){
        printf("send game packet protocol failed");
        return -1;
    }
    return 0;
}


int init_server(char *ip_address){

    struct sockaddr_in sockAdresse = {0};
    sockAdresse.sin_addr.s_addr = htonl(INADDR_ANY);
    sockAdresse.sin_port = htons(PORT);
    sockAdresse.sin_family = AF_INET;

    int myServSock = socket(AF_INET,SOCK_STREAM,6);
    if (myServSock < 0){
        perror("socket");
        close(myServSock);
        return 1;
    }

    if (bind(myServSock,(struct sockaddr *) &sockAdresse,sizeof(sockAdresse)) == -1){
        perror("bind");
        close(myServSock);
        return 1;
    }

    if (listen(myServSock,5) < 0){
        perror("listen");
        close(myServSock);
        return 1;
    }
    
    printf("Server start : \n");
    if (ip_address != NULL){
        int ret = init_connection_existant_game(ip_address);
        //TODO: need difference if is os_error or timeout
        if ( ret != 0){
            close(myServSock);
            return 1;
        }
    }
    game_server(myServSock);

    if (close(myServSock) == -1){
        perror("close socket:");
    }
    return 0;
}

int main(int argc, char const *argv[])
{

    return 0;
}
