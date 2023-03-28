#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <iconv.h>
#include <string.h>
#include <pthread.h>

#include "Message.h"

#define KEY 192002

typedef struct message {
    long message_type;
    char message_body[BUFFER_SIZE];
}message;


void send_msg_to_python_process(char* buffer);
char *read_msg_from_python_process();
int remove_enter_in_buffer(char* buffer);

void *receive_test(void *args) {
    while(1) {
        char* buffer = read_msg_from_python_process();
        printf("\nbuffer from py: %s\n", buffer);
    }
}

void *send_test(void *args) {
    while(1) {
        char* buffer = (char *)calloc(BUFFER_SIZE, sizeof(char));
        fgets(buffer, BUFFER_SIZE, stdin);
        send_msg_to_python_process(buffer);
    }
    
}

int main() {

    pthread_t send_thread;
    pthread_t read_thread;
    pthread_create(&send_thread, NULL, send_test, NULL);
    pthread_create(&read_thread, NULL, receive_test, NULL);

    pthread_join(send_thread, NULL);
    pthread_join(read_thread, NULL);

    return 0;
}

void send_msg_to_python_process(char* buffer) {
    int message_queueID = msgget(KEY, 0666 | IPC_CREAT);
    
    struct Message message;
    message.message_type = FROM_C_TO_PY;

    message.msg_body.object_type.typeObject = 1;
    message.msg_body.object_type.metaData = 2;
    message.msg_body.object_size = 10;
    message.msg_body.id_object = 1;
    message.msg_body.id_player = 2;

    buffer[strlen(buffer)] = '\n';
    strncpy(message.msg_body.data, buffer, BUFFER_SIZE);
    printf("\n%s\n", (char*)(message.msg_body.data));

    if (msgsnd(message_queueID, &message, sizeof(struct Msg_body), 0) == -1) {
        perror("msgsnd");
        exit(1);
    }

    printf("Message sent!\n");

}

char *read_msg_from_python_process() {
    //Open the message queue to communicate to process python. The message_queue has its integer identifier
    int message_queueID = msgget(KEY, 0666 | IPC_CREAT);
    // printf("\nmessage queue id: %d\n", message_queueID);

    message msg;

    // Receive the coor message type
    msg.message_type = FROM_PY_TO_C; 

    if(msgrcv(message_queueID, &msg, sizeof(msg), msg.message_type, 0) == -1) {
        perror("read msg failed from python process");
    }
    
    char* buffer = (char*)calloc(BUFFER_SIZE, 1);

    strncpy(buffer, msg.message_body, sizeof(msg.message_body));
    remove_enter_in_buffer(buffer);
    // printf("\nlen: %ld, msg from python: %s\n",strlen(buffer), buffer);
    return buffer;
}

int remove_enter_in_buffer(char* buffer) {
    int k;
    for(k = 0; k < BUFFER_SIZE; k++) {
        if(buffer[k] == '\n') {
            buffer[k] = '\0';
            break;
        }
    }
    return k;
}
