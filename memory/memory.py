from random import randint, shuffle
import string
import sys
import time
sys.path.insert(0, "/Users/clark/projects/grid_games")

from grid.grid import Grid
from grid.point import Point

class Memory(Grid):
    MATCHED_VALUE = '#'
    def __init__(self, num_rows, num_columns):
        super(Memory, self).__init__(num_rows=num_rows, num_columns=num_columns)
        self._populate_lettered_pairs()

    def _populate_lettered_pairs(self):
        if (self._num_rows * self._num_columns) % 2 != 0:
            print "invalid number of rows/columns"
            sys.exit()
        num_pairs = (self._num_rows * self._num_columns) / 2

        if num_pairs > 52:
            print "invalid number of rows/columns"
            sys.exit()

        # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        letters = string.letters

        all_pairs = [l for l in letters[:num_pairs]]
        all_pairs.extend(all_pairs)
        shuffle(all_pairs)

        for row_index, row in enumerate(self._grid):
            for column_index, point in enumerate(row):
                all_pairs_index = (row_index * self._num_columns) + column_index
                self.update_point(row=row_index, column=column_index, value=all_pairs[all_pairs_index], visible=False)

    def player_turn(self):
        print self.output(show_indicies=True)
        print self.output(show_indicies=True, hide_invisible=True)

        while True:
            user_point_one = self.get_user_input()
            if self.get_point(user_point_one).get_value() == Memory.MATCHED_VALUE:
                print "1Invalid guess; Please provide a valid point."
                continue

            user_point_two = self.get_user_input()
            if self.get_point(user_point_two).get_value() == Memory.MATCHED_VALUE:
                print "2Invalid guess; Please provide a valid point."
                continue

            break

        if self.get_point(user_point_one).get_value() == self.get_point(user_point_two).get_value():
            self.update_point(row=user_point_one.get_row(), column=user_point_one.get_column(), value=Memory.MATCHED_VALUE, visible=True)
            self.update_point(row=user_point_two.get_row(), column=user_point_two.get_column(), value=Memory.MATCHED_VALUE, visible=True)
        else:
            self.update_point(row=user_point_one.get_row(), column=user_point_one.get_column(), visible=True)
            self.update_point(row=user_point_two.get_row(), column=user_point_two.get_column(), visible=True)
            print self.output(show_indicies=True, hide_invisible=True)
            time.sleep(3)
            self.update_point(row=user_point_one.get_row(), column=user_point_one.get_column(), visible=False)
            self.update_point(row=user_point_two.get_row(), column=user_point_two.get_column(), visible=False)

        print self.output(show_indicies=True, hide_invisible=True)

    def player_won(self):
        return self.is_game_over()

    def is_game_over(self):
        for row in self._grid:
            for point in row:
                if point.get_value() != Memory.MATCHED_VALUE:
                    return False
        return True

    def play(self):
        while True:
            self.player_turn()
            if self.is_game_over():
                break

def main():
    m = Memory(num_rows=3, num_columns=2)
    m.play()

if __name__ == '__main__':
    main()
