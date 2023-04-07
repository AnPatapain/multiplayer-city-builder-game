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

    init_game_packet(ip_list_packet, GPP_RESP_IP_LIST, size_payload);
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

int connect_to_all_ip(const game_packet *resp_ips){
    game_ip *ips = (game_ip*) resp_ips->payload;
    int number_ips = (int) resp_ips->data_size / (int) sizeof(uint32_t);
    struct sockaddr_in sock_adresse = {0};
    sock_adresse.sin_port = htons(PORT);
    int new_socket;
    for (int i = 0; i < number_ips; i++){
        if (connection_existant_game(ips[i],FALSE) != 0){
            return -1;
        }
    }
    return 0;
}

int send_all_client(Object_packet *object){
    if (object == NULL){
        return -1;
    }
    game_packet *packet = encapsulate_object_packets(object,1,GPP_ALTER_GAME);
    client_game *client_to_send = first_client();
    while (client_to_send != NULL){
        if (send_game_packet(packet, client_to_send->socket_client) == -1){
            return -1;
        }
        client_to_send = client_to_send->next;
    }
    return 0;
}

int send_to_python(const game_packet *packet,int system_socket){
    if (packet == NULL){
        return -1;
    }
    int nb_object = 0;
    Object_packet *objects = uncap_object_packets(&nb_object,packet);
    print_object_packet(objects);
    printf("chaine :\n");
    write(1,objects->data,objects->object_size);
    printf("\n");
    for(int i = 0; i < nb_object; i++){
        if (send_object_packet(objects + i, system_socket) == -1){
            /*
            // Test: send data
            char *str = "{\"start\": [22, 39], \"end\": [22, 39], \"building_type\": 1001}";
            Object_packet *obj = new_object_packet();
            init_object_packet(obj,410, strlen(str));
            obj->id_object = 12;
            obj->data = str;
            send_all_client(obj);*/
            printf("error send to python\n");
            return -1;
        }
    }
    return 0;
}

int type_check(client_game *client, game_packet *packet, int system_socket) {
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
            return 0;
        case GPP_GAME_STATUS:
            //TODO: Send data to python
            return 0;
        case GPP_ALTER_GAME:
            /*{
                FILE *fichier = fopen("mon_gros_fichier-recep.txt","w");
                fwrite(packet->payload, packet->data_size, 1, fichier);
                fflush(fichier);
                fclose(fichier);
            }*/
            return send_to_python(packet,system_socket);
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
            return connect_to_all_ip(packet);
        case GPP_BAD_IDENT:
            printf("Error bad indent\n");
            return -1;
        default:
            printf("Error bad packet\n");
            return 0;
    }
}

int check_all_client(fd_set *fds, int socket_system) {
    client_game *client = first_client();
    game_packet *recv_packet = new_game_packet();
    while (client != NULL){
        if (FD_ISSET(client->socket_client, fds)){
            if (receive_game_packet(recv_packet,client->socket_client) == 0){
                printf("Client %i disconnect\n",client->player_id);
                close(client->socket_client);
                clg_remove(client);
                client = client->next;
                continue;
            }
            print_game_packet(recv_packet);
            if (type_check(client, recv_packet, socket_system) == -1){
                printf("Error check client %i\n",client->player_id);
            }
        }
        client = client->next;
    }
    free(recv_packet);
    return 0;
}

int game_server(int socket_listen, int socket_system) {
    fd_set fd_listen_sock;
    int number_fd;
    int max = 0;
    
    while (1){
        FD_ZERO(&fd_listen_sock);
        FD_SET(socket_listen, &fd_listen_sock);
        FD_SET(socket_system, &fd_listen_sock);

        cgl_set_all_client(&fd_listen_sock, &max);
        if (max < socket_system){
            max = socket_system;
        }
        if (max < socket_listen){
            max = socket_listen;
        }

        number_fd = select(max +1, &fd_listen_sock, NULL, NULL, NULL);

        if (number_fd < 0){
            perror("select :");
            return -1;
        }

        if (FD_ISSET(socket_listen, &fd_listen_sock)){
            if (accept_new_client(socket_listen) == NULL){
                return -1;
            }
            printf("LOG: new client_game accept\n");
        }
        if (FD_ISSET(socket_system, &fd_listen_sock)){
            Object_packet *python_packet = calloc(sizeof(Object_packet), 1);
            if (receive_object_packet(python_packet, socket_system) == 0){
                printf("Python Disconnect\n");
                return -1;
            }

            print_object_packet(python_packet);
            if (is_for_C(python_packet)){
                //TODO: C'est ecrit au dessus
            } else{
                if (send_all_client(python_packet) == -1){
                    printf("Error send packet\n");
                }
            }
            free(python_packet);
        }
        check_all_client(&fd_listen_sock, socket_system);
    }
}

int connection_existant_game(game_ip ip_address, bool is_new_player){

    // Create new socket
    struct sockaddr_in sock_adresse = {0};
    sock_adresse.sin_port = htons(PORT);
    sock_adresse.sin_addr.s_addr = ip_address;
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
            if (is_new_player)
                printf("Error can't connect to game\n");
            else{
                printf("Error connection at %s", inet_ntoa(sock_adresse.sin_addr));
            }
            close(new_socket);
            return 1;
        }

        if (receive_game_packet(connection, new_socket) == 0) {
            return 1;
        }
        print_game_packet(connection);
        if (connection->type == GPP_CONNECT_START){
            if (is_new_player) {
                new_payer_id();
                init_game_packet(connection, GPP_CONNECT_NEW, 0);
            } else{
                init_game_packet(connection, GPP_CONNECT_REQ, 0);
            }
            if (send_game_packet(connection, new_socket) < 1) {
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
    if (is_new_player) {
        init_game_packet(connection, GPP_ASK_IP_LIST, 0);
        if (send_game_packet(connection, new_client->socket_client) < 1) {
            printf("send game packet protocol failed\n");
            return -1;
        }
    }
    /**
     *  aled
     *
    int ma_grosse_taille = 4703127;
    char *mes_grosses_donnee = malloc(sizeof(char) * ma_grosse_taille);
    FILE* mon_gros_fichier = fopen("mon_gros_fichier-send.txt","w");
    FILE* urandom = fopen("/dev/urandom","r");
    fread(mes_grosses_donnee,ma_grosse_taille,1,urandom);
    fwrite(mes_grosses_donnee, ma_grosse_taille, 1, mon_gros_fichier);
    fflush(mon_gros_fichier);
    fclose(mon_gros_fichier);
    game_packet *mon_gros_packet = new_game_packet();
    init_game_packet(mon_gros_packet, GPP_ALTER_GAME, ma_grosse_taille);
    // PENSEZ A METTRE SES GROSSE DONNEE DANS SON PACKET CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
    mon_gros_packet->payload = mes_grosses_donnee;
    send_game_packet(mon_gros_packet,new_client->socket_client);
    free(mes_grosses_donnee);
    */

    return 0;
}

int init_system_socket(){
    int socket_system = socket(AF_LOCAL,SOCK_STREAM,0);
    struct sockaddr_un sock_addr_system = {0};

    memcpy(sock_addr_system.sun_path, SYSSOCK,sizeof(SYSSOCK) -1);
    sock_addr_system.sun_family = AF_LOCAL;

    if (connect(socket_system,(struct sockaddr*) &sock_addr_system, sizeof(sock_addr_system)) == -1){
        perror("connect system");
        return -1;
    }

    if (throw_new_object(GOP_CONNECT, socket_system) == -1){
        return -1;
    }
    return socket_system;
}

int init_server(const char *ip_address){

    if (ip_address != NULL){
        struct sockaddr_in new_sock;
        if (inet_aton(ip_address,&(new_sock.sin_addr)) == 0){
            printf("Erreur : inet_aton %s \n",ip_address);
            return -1;
        }
        int ret = connection_existant_game(new_sock.sin_addr.s_addr,TRUE);
        //TODO: need difference if is os_error or timeout (notify python)
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
    /*int system_sock = init_system_socket();
    if (system_sock == -1){
        close(listen_socket);
        return 1;
    }*/
    game_server(listen_socket, 1);

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

    /**
     * encapsulation test
     */

    /*char *str = "Mon gros payload";
    char *str2 = "Mon moins grand payload";
    Object_packet *obj1 = calloc(sizeof(Object_packet),2);
    init_object_packet(obj1,250,strlen(str) + 1);
    init_object_packet(obj1 + 1, 3, strlen(str2) + 1);

    obj1[0].data = str;
    obj1[1].data = str2;

    printf("test: %s\n",obj1[0].data);
    printf("test2: %s\n",obj1[1].data);
    print_object_packet(obj1);
    print_object_packet(obj1 + 1);

    game_packet *gp1 = encapsulate_object_packets(obj1, 2, GPP_ALTER_GAME);
    print_game_packet(gp1);

    int nb = 0;
    Object_packet *obj_res = uncap_object_packets(&nb,gp1);
    print_object_packet(obj_res);
    print_object_packet(obj_res + 1);
    printf("test recu: %s\n",obj_res[0].data);
    printf("test recu: %s\n",obj_res[1].data);*/


    return init_server(ip);
}
