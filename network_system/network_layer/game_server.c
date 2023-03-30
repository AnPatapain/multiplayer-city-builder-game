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

    game_packet *connection = new_game_packet(GPP_CONNECT_NEW);
    if (connection == NULL){
        return -1;
    }
    connection->payload = NULL;

    if (send_game_packet(connection,0,new_socket) < 1){
        printf("send game packet protocol failed");
        return -1;
    }

    //TODO: Select with timeout

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
        if (init_connection_existant_game(ip_address) < 0){
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
