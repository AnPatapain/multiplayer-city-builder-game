#include "Message.h"

const uint32_t header_size = sizeof(Object_packet) - sizeof(char*);
//const uint32_t header_size = 14;

int main() {
    int sockfd;
    struct sockaddr_un serv_addr;
    
    // Create AF_UNIX socket
    sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }
    
    // Set server address
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sun_family = AF_UNIX;
    strncpy(serv_addr.sun_path, "/tmp/socket", sizeof(serv_addr.sun_path) - 1);
    
    // Connect to the server
    if (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("connect");
        return 1;
    }

    // char* buffer = (char*)calloc(1024, 1);
    Object_packet objectPacket;
    if(recv(sockfd, &objectPacket, header_size, 0) == -1) {
        perror("error");
    }

    printf("%i / %i\n",header_size,objectPacket.object_size);
    if ( objectPacket.object_size > 0 ){
        objectPacket.data = calloc(objectPacket.object_size,1);
        recv(sockfd,objectPacket.data,objectPacket.object_size,MSG_WAITALL);
    }
    printf("\n%s\n", objectPacket.data);
    // Close the socket
    close(sockfd);

    return 0;
}
