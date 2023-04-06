#ifndef GAME_PACKET_PROTOCOL
#define GAME_PACKET_PROTOCOL
#define GPP_DEBUG

#include <stdint.h>

#include "message_type.h"

#ifdef GPP_DEBUG
#include <stdio.h>
#endif

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

void print_packet(const game_packet *packet);

game_packet* new_game_packet();
int new_payer_id();
int throw_new_packet(uint8_t type, int socket);
void init_packet(game_packet *packet, uint8_t type, uint32_t size_payload);
int send_game_packet(const game_packet *send_packet, int socket);
int receive_game_packet(game_packet *recv_packet, int socket);


#endif //GAME_PACKET_PROTOCOL