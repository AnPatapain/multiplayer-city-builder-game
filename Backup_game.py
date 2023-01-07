import pickle
from os import mkdir,path

from game import game


class Backup_game:
    def __init__(self):
        self.dir = "Saved_games/"

    def load_game(self, backup_name):
        path_game = self.dir + backup_name
        if not path.exists(path_game):
            print("game does not exists")
            return None
        file= open(path_game, "rb")
        game = pickle.load(file)
        file.close()
        return game

    def save_game(self, game, backup_name):
        path_game = self.dir + backup_name
        if not path.exists(self.dir):
            mkdir(self.dir)
        file = open(path_game, "wb")
        pickle.dump(game, file)
        file.close()
        return game