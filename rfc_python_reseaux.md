# Protocole réseau 

# Sommaire
- Structure réseau
- Protocole principaux
    - Game packets protocol (GPP)
    - Object Transfert protocol (OTP)

- Protocole de découverte
    - Unicast discorery
    - Broadcast discovery


# Structure réseau


# Protocole principaux
## Game Packet protocol
### objectif 

Ce protocole sert a communiquer entre les client à travers le réseau. Il  doit être reçu et envoyé par les processus C a travers les sockets TCP.


## Header structure
### Type
Entier non-signé de 1 octet, il sert à décrire le type de donnée présente dans le payload.

#### Type connue
- `11: ASK_GAME_STATUS`: Demande à un client l'états de l'ensemble des objets lui appartenant. Le payload est inutile et le champ `data_size` doit être défini à `0`.
- `12: GAME_STATUS`: Réponse à `ASK_GAME_STATUS`. L'ensemble des objet sont dans le payload sous format OTP.
- `20: ALTER_GAME`: La plus commune des requête; un client envoie de nouvelles donnée pour des entités définie dans le payload (format OTP).
- `30: DELEGATE_ASK`: Demande à un autre client s'il peut reprendre, en partie ou totalement, la gestion de ses données. Le payload doit contenir l'ensemble des objets à transmettre au format OTP.
- `31: DELEGATE_OK`: Réponse au `DELEGATE_ASK` l'utilisateur a ses donnés. 
- `50: ASK_IP_LIST`: Demande la liste des IP connue à un utilisateur.Le payload est inutile et le champ `data_size` doit être défini à `0`.
- `51: RESP_IP_LIST`: Réponse à la demande `ASK_IP_LIST`.Le champ `data_size` contient le nombre d'adresse IP connue et le payload contient la liste des adresses ips.




### schéma
- Type: 1 octet: Type de de donnée envoyée
- player_id: 2 octets: Identifiant Unique du joueur
- reserved: Padding
- data_size: taille **en octets** du payload
- id_event: identifiant unique de l'évènement 
```
   0             8             16             24            32
  0|---------------------------------------------------------|\
   |   Type      |         player_id          |  reserved    | \
  1|---------------------------------------------------------| |
   |                       data_size                         | | -> Header
  2|---------------------------------------------------------| |
   |                       id_event                          | /
  3|---------------------------------------------------------|/
   |                                                         |
   |                        payload                          |
   |                                                         |
  n|---------------------------------------------------------|
```
