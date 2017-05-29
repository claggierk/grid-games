import sys


class Player(object):
    def __init__(self, name):
        self._name = name
        self._score = 0

    def get_name(self):
        return self._name

    @staticmethod
    def quit(name):
        print("{} quit ... game over :-(".format(name))
        sys.exit()
