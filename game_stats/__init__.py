import pickle

class GameStats:

    def __init__(self, upsettings):
        self.upsettings = upsettings
        self.reset_stats()
        self.game_active = False
        self.highest_score = 0

    def reset_stats(self):
        self.ships_left = self.upsettings.ship_limit
        self.score = 0
        self.level = 1

    def save_highest_score(self):
        highest = open("highest_score.pkl", 'wb')
        pickle.dump(str(self.highest_score), highest, 0)
        highest.close()

    def load_highest_score(self):
        highest = open("highest_score.pkl", 'rb')
        try:
            str_highest_score = pickle.load(highest)
            self.highest_score = int(str_highest_score)
        except EOFError:
            self.highest_score = 222
        finally:
            highest.close()

