class Game(object):
    def player_turn(self):
        pass

    def is_valid_guess(self):
        pass

    def is_invalid_guess(self):
        return not self(is_valid_guess)

    def is_game_over(self):
        pass

    def play(self):
        pass

if __name__ == '__main__':
    print "Game (generic) main"
