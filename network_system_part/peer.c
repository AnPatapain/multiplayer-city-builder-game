#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <iconv.h>
#include <string.h>
#include <pthread.h>

#define BUFFER_SIZE 1024
#define COOR_MESSAGE_TYPE 1
#define FROM_PY_TO_C 2
#define FROM_C_TO_PY 3
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
    // send_test();
    // receive_test();
    pthread_t send_thread;
    pthread_t read_thread;
    pthread_create(&send_thread, NULL, receive_test, NULL);
    pthread_create(&read_thread, NULL, send_test, NULL);

    pthread_join(send_thread, NULL);
    pthread_join(read_thread, NULL);

    return 0;
}

void send_msg_to_python_process(char* buffer) {
    //Open the message queue to communicate to process python. The message_queue has its integer identifier
    int message_queueID = msgget(KEY, 0666 | IPC_CREAT);
    // printf("\nmessage queue id: %d\n", message_queueID);

    message msg;
    msg.message_type = FROM_C_TO_PY;
    buffer[strlen(buffer)] = '\n';
    strncpy(msg.message_body, buffer, BUFFER_SIZE);

    // printf("\n%s - sent to python\n", msg.message_body);
    if(msgsnd(message_queueID, &msg, sizeof(msg), 0) == -1) {
        perror("send msg failed to python process");
    }
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