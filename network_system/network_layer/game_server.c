#include "game_server.h"


client_game* accept_new_client(int socket_listen){
    client_game* new_client = calloc(1,sizeof(client_game));

    if (new_client == NULL){
        perror("Calloc");
        return NULL;
    }
    new_client->player_id = 0;
    printf("accept new client\n");
    uint len = sizeof(struct sockaddr_in);
    if ((new_client->socket_client = accept(socket_listen,(struct sockaddr*) &(new_client->sockaddr_client),&len)) <= 0){
        perror("accept");
        return NULL;
    }
    new_client->as_initial = TRUE;

    if (cgl_append(new_client) < 0){
        return NULL;
    }

    if (throw_new_packet(GPP_CONNECT_START,new_client->socket_client) == -1){
        printf("error send accept");
    }
    return new_client;
}

client_game* add_client(int socket_client){
    client_game* new_client = calloc(1,sizeof(client_game));
    
    if (new_client == NULL){
        perror("Calloc");
        return NULL;
    }
    new_client->player_id = 0;
    new_client->socket_client = socket_client;
    new_client->as_initial = TRUE;
    
    if (cgl_append(new_client) < 0){
        return NULL;
    }
    return new_client;
}

int new_connection(client_game *client, const game_packet *packet){
    if (id_exist(client, packet->player_id)){
        if (throw_new_packet(GPP_BAD_IDENT,client->socket_client) < 0){
            return -1;
        }
        return 0;
    }
    return req_connection(client,packet);
}

int req_connection(client_game *client, const game_packet *packet){
    client->player_id = packet->player_id;
    if (throw_new_packet(GPP_CONNECT_OK,client->socket_client) < 0){
        return -1;
    }
    return 0;
}

int get_ip_list(client_game *client){
    game_packet *ip_list_packet = new_game_packet();
    int number_ip;
    game_ip *ips = get_all_ips(&number_ip, client);
    int size_payload = (int) number_ip * (int) sizeof(uint32_t);

    init_packet(ip_list_packet, GPP_RESP_IP_LIST, size_payload);
    ip_list_packet->payload = (char *) ips;

    if (send_game_packet(ip_list_packet,client->socket_client) <= 0){
        return -1;
    }
    free(ip_list_packet);
    free(ips);
    return 0;
}

void show_list_ip(const game_packet *packet){
    game_ip *ips = (game_ip*) packet->payload;
    int number_ips = (int) packet->data_size / (int) sizeof(uint32_t);
    struct in_addr address  = {0};
    printf("number ips: %i\n", number_ips);
    for (int i = 0; i < number_ips; i++){
        address.s_addr = ips[i];
        printf("address found : %s\n", inet_ntoa(address));
    }
}

int type_check(client_game *client,game_packet *packet){
    switch (packet->type) {
        case GPP_CONNECT_NEW:
            return new_connection(client,packet);
        case GPP_CONNECT_REQ:
            return req_connection(client,packet);
        case GPP_CONNECT_OK:
            client->player_id = packet->player_id;
            //TODO: contact all ips
            return 0;
        case GPP_ASK_GAME_STATUS:
            //TODO: Request python for all game
            return 0;
        case GPP_GAME_STATUS:
            //TODO: Send data to python
            return 0;
        case GPP_ALTER_GAME:
            //TODO: Send data to python
            return 0;
        case GPP_DELEGATE_ASK:
            //TODO: Notify python to take own of this data
            return 0;
        case GPP_DELEGATE_OK:
            //TODO: Python take data
            return 0;
        case GPP_ASK_IP_LIST:
            return get_ip_list(client);
        case GPP_RESP_IP_LIST:
            show_list_ip(packet);
            return 0;
        case GPP_BAD_IDENT:
            //TODO: (implement bad request + log)?
            return 0;
        default:
            //TODO: (implement bad request + log)?
            return 0;
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
            print_packet(recv_packet);
            if (type_check(client,recv_packet) == -1){
                printf("Error check client %i\n",client->player_id);
            }
        }
        client = client->next;
    }
    free(recv_packet);
    return 0;
}

int game_server(int socket) {
    fd_set fd_listen_sock;
    int number_fd;
    int max = socket;
    
    while (1){
        FD_ZERO(&fd_listen_sock);
        FD_SET(socket, &fd_listen_sock);

        cgl_set_all_client(&fd_listen_sock, &max);
        number_fd = select(max +1, &fd_listen_sock, NULL, NULL, NULL);

        if (number_fd < 0){
            perror("select :");
            return -1;
        }

        if (FD_ISSET(socket,&fd_listen_sock)){
            if (accept_new_client(socket) == NULL){
                return -1;
            }
            printf("LOG: new client_game accept\n");
        }
        check_all_client(&fd_listen_sock);
    }
}

int init_connection_existant_game(const char *ip_address){

    // Create new socket
    struct sockaddr_in sock_adresse = {0};
    sock_adresse.sin_port = htons(PORT);

    if (inet_aton(ip_address,&(sock_adresse.sin_addr)) == 0){
        printf("Erreur : inet_aton %s \n",ip_address);
        return -1;
    }
    sock_adresse.sin_family = AF_INET;

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

    game_packet *connection = new_game_packet();
    if (connection == NULL){
        return -1;
    }
    connection->payload = NULL;

    // Start protocol connection
    struct timeval timeout = {0};
    fd_set fd_set_connect;

    do {

        timeout.tv_sec = TIMEOUT;

        FD_ZERO(&fd_set_connect);
        FD_SET(new_socket, &fd_set_connect);
        select(new_socket + 1, &fd_set_connect, NULL, NULL, &timeout);

        if (!FD_ISSET(new_socket, &fd_set_connect)) {
            printf("Error can't connect to game\n");
            close(new_socket);
            return 1;
        }

        if (receive_game_packet(connection, new_socket) == 0) {
            return 1;
        }
        print_packet(connection);
        if (connection->type == GPP_CONNECT_START){
            new_payer_id();
            init_packet(connection, GPP_CONNECT_NEW, 0);
            if (send_game_packet(connection,new_socket) < 1){
                printf("send game packet protocol failed\n");
                return -1;
            }
            // Need to reloop
            connection->type = GPP_BAD_IDENT;
        }

    }while (connection->type == GPP_BAD_IDENT);

    if (connection->type != GPP_CONNECT_OK){
        printf("Error bad connection type\n");
        close(new_socket);
        return -1;
    }

    // Add client to list
    client_game *new_client = add_client(new_socket);
    new_client->player_id = connection->player_id;
    new_client->sockaddr_client = sock_adresse;
    printf("Event: %i: Connected to client %i\n",connection->id_event,new_client->player_id);

    // Ask for ip
    init_packet(connection, GPP_ASK_IP_LIST, 0);
    if (send_game_packet(connection,new_client->socket_client) < 1){
        printf("send game packet protocol failed\n");
        return -1;
    }
    return 0;
}


int init_server(const char *ip_address){

    if (ip_address != NULL){
        int ret = init_connection_existant_game(ip_address);
        //TODO: need difference if is os_error or timeout
        if ( ret != 0){
            return 1;
        }
    }else{
        new_payer_id();
    }

    struct sockaddr_in listen_socket_addr = {0};
    listen_socket_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    listen_socket_addr.sin_port = htons(PORT);
    listen_socket_addr.sin_family = AF_INET;

    int listen_socket = socket(AF_INET, SOCK_STREAM, 6);
    if (listen_socket < 0){
        perror("socket");
        close(listen_socket);
        return 1;
    }

    if (bind(listen_socket, (struct sockaddr *) &listen_socket_addr, sizeof(listen_socket_addr)) == -1){
        perror("bind");
        close(listen_socket);
        return 1;
    }

    if (listen(listen_socket, 5) < 0){
        perror("listen");
        close(listen_socket);
        return 1;
    }
    
    printf("Server start : \n");

    game_server(listen_socket);

    if (close(listen_socket) == -1){
        perror("close socket:");
    }
    return 0;

}

int main(int argc, char const *argv[])
{
    const char *ip = NULL;
    if (argc > 1){
        ip = argv[1];
    }

    init_server(ip);



    return 0;
}
