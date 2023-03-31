#ifndef GAME_PACKET_PROTOCOL
#define GAME_PACKET_PROTOCOL

#include <stdint.h>

#include "message_type.h"

#define PORT 5080

struct game_packet
{
    uint8_t type;
    uint16_t player_id;
    uint8_t reserved;
    uint32_t data_size;
    uint32_t id_event;
    char* payload;
};

typedef struct game_packet game_packet;
typedef uint32_t game_ip;


game_packet* new_game_packet();
int throw_new_packet(uint8_t type,int socket);
void init(game_packet *packet,uint8_t type, uint32_t size_payload);
int send_game_packet(game_packet *send_packet, int socket);
int receive_game_packet(game_packet *recv_packet, int socket);


#endif //GAME_PACKET_PROTOCOL