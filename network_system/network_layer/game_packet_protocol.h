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


game_packet* new_game_packet(uint8_t type);
int send_game_packet(game_packet *packet, int size_payload, int socket);


#endif //GAME_PACKET_PROTOCOL