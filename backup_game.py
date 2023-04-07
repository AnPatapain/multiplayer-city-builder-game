import os
import lzma
import pickle
from os import mkdir,path
from game.game_controller import GameController
from network_system.system_layer.read_write import SystemInterface

save_dir = "saved_games/"
list_fichiers = os.listdir(save_dir)
def load_game(backup_name):
    path_game = save_dir + backup_name
    if not path.exists(path_game):
        print("game does not exists")
        return None
    file = lzma.open(path_game, "rb")
    GameController.get_instance().__dict__ = pickle.load(file)
    GameController.get_instance().save_load()
    file.close()

def save_game(backup_name):
    path_game = save_dir + backup_name
    if not path.exists(save_dir):
        mkdir(save_dir)
    file = lzma.open(path_game, "wb")
    pickle.dump(GameController.get_instance().__dict__, file)

    # ---------------------------- TEST --------------------------------
    read_write_py_c = SystemInterface.get_instance()
    serialize_data = pickle.dumps(GameController.get_instance().__dict__)
    read_write_py_c.send_message(id_player=1, command=2, id_object=3, data=serialize_data, encode=False)
    # -------------------------- FIN TEST ------------------------------

    file.close()