#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BUFFER_SIZE 1024
#define COOR_MESSAGE_TYPE 1
#define FROM_PY_TO_C 2
#define FROM_C_TO_PY 3


struct Object_type {
    uint16_t typeObject;
    uint16_t metaData;
};


struct Msg_body {
    struct Object_type object_type;
    uint32_t object_size;
    uint32_t id_object;
    uint16_t id_player;
    char data[BUFFER_SIZE];
};

struct Message
{
    long message_type; // MSG_TYPE_FROM_C_TO_PY || MSG_TYPE_FROM_PY_TO_C
    struct Msg_body msg_body;
};
