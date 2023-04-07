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
## Game Packet Protocol (GPP)
### objectif 

Ce protocole sert à communiquer entre les clients à travers le réseau. Il doit être reçu et envoyé par les processus C à travers des sockets TCP.

Port **5252**

### Initialisation de la connexion
Un client souhaite se connecter au jeu:

-> Il génère un nouvel id puis et récupère une adresse IP d'un joueur connecté au jeu.

-> Demande, à cette IP, une connexion avec le paquet `CONNECT_NEW`. 

-> Les joueurs répond avec un paquet `RESP_IP_LIST` avec la liste des IP des joueurs connectés. Ou si l'id du client est déjà utilisée, répond avec `BAD_IDENT` et le client reprend la processus du début.

-> Le client envoie une requête `CONNECT_REQ` à toutes les IPs obtenues précédemment. Afin de s'enregistrer auprès de tout les joueurs connectés;

-> Chaque joueur répond avec `CONNECT_OK`, pour signaler qu'il a enregistré sa demande de connection.

-> Une fois la connection avec chaque joueur établie le client demande à chaque joueur les instances de leurs objets avec `ASK_GAME_STATUS`


## Header structure
### Type
Entier non-signé de 1 octet (uint_8).
Il sert à décrire le type de donnée présente dans le payload.

#### Type connus: 
#### `1: CONNECT_NEW`
Demande une connexion à un jeu en cours. Le payload est inutile et le champ `data_size` doit être défini à `0`. Le champs id doit contenir l'identifiant unique généré.
#### `2: CONNECT_REQ`
Demande une connexion à un client du jeu
#### `3: CONNECT_OK`
Réponse à `CONNECT_REQ`, le nouveau client à été enregistré.
#### `4: GPP_CONNECT_START`
Nouveau packet: Après l'acceptation d'un socket client le joueur envoye un packet pour affirmer au client nouvelement connecté
qu'il peut commencer a envoyer des informations.
#### `20: ALTER_GAME`
La plus commune des requêtes; un client envoie de nouvelles données pour des entités définies dans le payload (format OTP).
#### `50: ASK_IP_LIST`
Demande la liste des IP connue à un utilisateur. Le payload est inutile et le champ `data_size` doit être défini à `0`.
#### `51: RESP_IP_LIST`
Réponse à la demande `ASK_IP_LIST`. Le champ `data_size` contient le nombre d'adresses IP connue et le payload contient la liste des adresses ips et des `player_id`.
#### `52: BAD_IDENT`
L'identifiant reçu dans `ASK_LIST_IP` est indisponible (il existe déjà). 

### player_id
entier non-signé 16bits (uint_16).
Le player_id est un identifiant de 16bits (2 octets). Cet identifiant doit être unique et défini aléatoirement. 

### data_size
Entier non-signé de 32bits (uint_32).
Taille du payload en octets (Bytes)

### id_event
Entier non-signé de 32bits (uint_32).
Identifiant de l'évènement, peut être incrémentale.

### schéma
- Type: 1 octet: Type de donnée envoyée
- player_id: 2 octets: Identifiant Unique du joueur
- reserved: (Padding)
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

## Object Transfert Protocol (OTP)

### Objectif

Transférer des objects de du C vers l'instance Python du jeu.

## Header structure
### command
Precise le type de packet. Si la commande est pour le C le packet sera intercepté

### object_size
Entier non-signé de 32bits (uint_32).
Taille du data_object en octets (Bytes)

### id_object
Entier non-signé de 32bits (uint_32).
Identifiant unique de l'objet généré aléatoirement à sa création

### player_id
entier non-signé 16bits (uint_16).
Le player_id est un identifiant de 16bits (2 octets). Cet identifiant doit être unique et défini aléatoirement. 

```
   0             8             16             24            32
  0|---------------------------------------------------------|\
   |        player_id          |           command           | \
  1|---------------------------------------------------------| |
   |                     object_size                         | | -> Header
  2|---------------------------------------------------------| |
   |                        id_object                        | /
  3|---------------------------------------------------------|/
   |                                                         |
   |                       data_object                       |
   |                                                         |
  n|---------------------------------------------------------|
```

| Command name    | Code |
|-----------------|------|
| Connect         | 400  |
| Disconnect      | 401  |
| Game save       | 402  |
|                 |      |
| Build           | 410  |
| Delete building | 411  |
| Risk update     | 412  |
|                 |      |
| Update walker   | 420  |
| Spawn walker    | 421  |
| Delete walker   | 422  |
|                 |      |
| Delegate?       | 499  |

 