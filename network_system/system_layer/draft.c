#define MSG_TYPE_FROM_C_TO_PY 1
#define MSG_TYPE_FROM_PY_TO_C 2


struct Object_type {
    long type;
    long subtype;
    // quel type pour metadata ? char* non ?
    char *metadata;
};

struct Data {
    long id_player;
    char *data;
};

struct Msg_body {
    struct Object_type object_Type;
    long data_size;
    long id_object;
    struct Data data;
};

struct Message
{
    long message_type; // MSG_TYPE_FROM_C_TO_PY || MSG_TYPE_FROM_PY_TO_C
    struct Msg_body msg_body;

};
