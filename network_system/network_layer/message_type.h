
/**
 * Demande une connexion à un jeu en cours. Le payload est inutile et le champ `data_size` doit être défini à `0`. Le champs id doit contenir l'identifiant unique généré.
*/
#define GPP_CONNECT_NEW 1

/**
 * Demande une connexion à un client du jeu
 * */
#define GPP_CONNECT_REQ 2

/**
 * Réponse à `CONNECT_REQ`, le nouveau client à été enregistré.
 * */
#define GPP_CONNECT_OK 3

/**
 * Nouveau packet: Après l'acceptation d'un socket client le joueur envoye un packet pour affirmer au client nouvelement connecté
 * qu'il peut commencer a envoyer des informations.
 **/
#define GPP_CONNECT_START 4

/**
 * Demande à un client l'états de l'ensemble des objets lui appartenant. Le payload est inutile et le champ `data_size` doit être défini à `0`.
 * */
#define GPP_ASK_GAME_STATUS 11

/**
 * Réponse à `ASK_GAME_STATUS`. L'ensemble des objet sont dans le payload sous format OTP.
 * */
#define GPP_GAME_STATUS 12

/**
 * La plus commune des requête; un client envoie de nouvelles donnée pour des entités définie dans le payload (format OTP).
 * */
#define GPP_ALTER_GAME 20

/**
 * Demande à un autre client s'il peut reprendre, en partie ou totalement, la gestion de ses données. Le payload doit contenir l'ensemble des objets à transmettre au format OTP.
 * */
#define GPP_DELEGATE_ASK 30

/**
 * Réponse au `DELEGATE_ASK` l'utilisateur a ses donnés. 
 * */
#define GPP_DELEGATE_OK 31

/**
 * Demande la liste des IP connue à un utilisateur. Le payload est inutile et le champ `data_size` doit être défini à `0`. Le champ ip doit
 * */
#define GPP_ASK_IP_LIST 50

/**
 * Réponse à la demande `ASK_IP_LIST`.Le champ `data_size` contient le nombre d'adresse IP connue et le payload contient la liste des adresses ips et des `player_id`.
 * */
#define GPP_RESP_IP_LIST 51

/**
 * L'identifiant reçu dans `ASK_LIST_IP` est indisponible (il existe déjà). 
 * */
#define GPP_BAD_IDENT 52
