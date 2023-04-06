#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include "Message.h"


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
    
    // Send data to the server
    char *message = "Hello, Python!";
    if (send(sockfd, message, strlen(message), 0) < 0) {
        perror("send");
        return 1;
    }

    // Receive response from the server
    char buffer[256];
    int n = recv(sockfd, buffer, sizeof(buffer), 0);
    if (n < 0) {
        perror("read");
        return 1;
    }
    printf("%s\n", buffer);
    
    // Close the socket
    close(sockfd);

    return 0;
}
