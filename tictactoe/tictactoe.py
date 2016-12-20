from random import randint
import sys
sys.path.insert(0, "/Users/clark/projects/grid_games")

from grid.grid import Grid
from grid.point import Point

class TicTacToe(Grid):
    SQUARE_SIDE = 3

    def __init__(self):
        super(TicTacToe, self).__init__(TicTacToe.SQUARE_SIDE, TicTacToe.SQUARE_SIDE)

    def player_turn(self):
        while True:
            user_point = self.get_user_point()
            if self.is_point_valueless(user_point):
                break
            print "Invalid guess; Please provide a valid point."
        user_point.set_value('X')
        self.set_point(user_point)

    def computer_turn(self):
        empty_points = self.get_empty_points()
        random_index = randint(0, len(empty_points)-1)
        computer_point = empty_points[random_index]
        computer_point.set_value('O')
        self.set_point(computer_point)

    def is_game_over(self):
        if self._won():
            return True
        if self._is_cats():
            return True
        return False

    def _is_cats(self):
        for row in self._grid:
            for point in row:
                if not point.get_value():
                    return False
        print self
        print " ***** CATS! *****"
        return True

    def _won(self):
        win_groups = [
            # horizontal wins
            [Point(row=0, column=0), Point(row=0, column=1), Point(row=0, column=2)],
            [Point(row=1, column=0), Point(row=1, column=1), Point(row=1, column=2)],
            [Point(row=2, column=0), Point(row=2, column=1), Point(row=2, column=2)],

            # vertical wins
            [Point(row=0, column=0), Point(row=1, column=0), Point(row=2, column=0)],
            [Point(row=0, column=1), Point(row=1, column=1), Point(row=2, column=1)],
            [Point(row=0, column=2), Point(row=1, column=2), Point(row=2, column=2)],

            # diagonal wins
            [Point(row=0, column=0), Point(row=1, column=1), Point(row=2, column=2)],
            [Point(row=0, column=2), Point(row=1, column=1), Point(row=2, column=0)],
        ]

        for win_group in win_groups:
            grid_win_point_values = map(lambda win_point: self.get_point(win_point).get_value(), win_group)
            if all(grid_win_point_values) and grid_win_point_values[0] == grid_win_point_values[1] == grid_win_point_values[2]:
                print self
                print " ***** {} won! *****".format(grid_win_point_values[0])
                return True
        return False

    def __repr__(self):
        return \
            "       Column\n"\
            "     1   2   3\n"\
            "  1  {} | {} | {}\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(row=0)]) +\
            "R   ---|---|---\n"\
            "o 2  {} | {} | {}\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(row=1)]) +\
            "w   ---|---|---\n"\
            "  3  {} | {} | {}\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(row=2)])

    def play(self):
        while True:
            print self
            self.player_turn()
            if self.is_game_over():
                break
            self.computer_turn()
            if self.is_game_over():
                break

def main():
    ttt = TicTacToe()
    ttt.play()

if __name__ == '__main__':
    main()
