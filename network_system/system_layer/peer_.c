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

    // Read header
    Object_packet objectPacket_read;
    if(recv(sockfd, &objectPacket_read, header_size, 0) == -1) {
        perror("error");
    }

    printf("%i / %i\n", header_size, objectPacket_read.object_size);

    // Read the actual data if the object_size > 0
    if (objectPacket_read.object_size > 0 ){
        objectPacket_read.data = (char *)calloc(objectPacket_read.object_size + 1, 1);
        recv(sockfd, objectPacket_read.data, objectPacket_read.object_size, MSG_WAITALL);
    }
    printf("\n%s\n", objectPacket_read.data);

    Object_packet objectPacket_write;
    char buffer[] = "Hello Python Je suis C";
    objectPacket_write.object_type.typeObject = 1;
    objectPacket_write.object_type.metaData = 2;
    objectPacket_write.object_size = strlen(buffer);
    objectPacket_write.id_object = 3;
    objectPacket_write.id_player = 4;
    objectPacket_write.data = (char *)calloc(strlen(buffer) + 1, 1);
    strncpy(objectPacket_write.data, buffer, strlen(buffer));
    send(sockfd, &objectPacket_write, sizeof(objectPacket_write), 0);

    // Close the socket
    close(sockfd);

    return 0;
}
