from random import randint, shuffle
import string
import sys
import time
sys.path.insert(0, "/Users/clark/projects/grid_games")

from grid.grid import Grid
from grid.point import Point

class Minesweeper(Grid):
    MINE = '*'

    def __init__(self, level='easy'):
        if level == 'easy':
            self.side = 10
            self.num_mines = 10
        elif level == 'intermediate':
            self.side = 15
            self.num_mines = 30
        elif level == 'expert':
            self.side = 20
            self.num_mines = 75
        else:
            self.side = 3
            self.num_mines = 3
        super(Minesweeper, self).__init__(num_rows=self.side, num_columns=self.side)
        self._populate_mines()
        self._compute_mine_neighbors()

    def _populate_mines(self):
        mines_placed = 0
        while True:
            row = randint(0, self.side - 1)
            column = randint(0, self.side - 1)
            point = Point(row=row, column=column, value=Minesweeper.MINE)

            if self.get_point(point).get_value() != Minesweeper.MINE:
                self.set_point(point)
                mines_placed += 1
                if mines_placed == self.num_mines:
                    break

    def _get_num_mine_neighbors(self, point):
        num_mine_neighbors = 0
        for neighbor in self.get_neigbors(point, boundaries=True):
            if neighbor.get_value() == Minesweeper.MINE:
                num_mine_neighbors += 1
        return num_mine_neighbors

    def _compute_mine_neighbors(self):
        for row_index, row in enumerate(self._grid):
            for column_index, point in enumerate(row):
                if point.get_value() == Minesweeper.MINE:
                    continue

                num_neighbor_mines = self._get_num_mine_neighbors(point)
                self.update_point(row=row_index, column=column_index, value=num_neighbor_mines)

    def player_turn(self):
        print self.output(show_indicies=True)
        print self.output(show_indicies=True, hide_invisible=True)

        while True:
            user_point = self.get_user_input()
            if user_point.is_visible():
                continue
            else:
                break

        user_grid_point = self.get_point(user_point)

        if user_grid_point.get_value() == Minesweeper.MINE:
            print "... IN A MINE!"
            self.update_point(row=user_grid_point.get_row(), column=user_grid_point.get_column(), visible=True)
            sys.exit()
        elif user_grid_point.get_value() == 0:
            self._expand_zeros(user_grid_point)

        print self.output(show_indicies=True, hide_invisible=True)

    def _expand_zeros(self, point):
        # base case - if you encounter a point that is already visible, STOP!
        if self.get_point(point).is_visible():
            return

        self.update_point(row=point.get_row(), column=point.get_column(), visible=True)

        for neighbor in self.get_neigbors(point, boundaries=True):
            neighbor_point = self.get_point(neighbor)
            if neighbor_point.get_value() == 0:
                # recursive call on 0
                self._expand_zeros(neighbor_point)
            else:
                # reveal the number cell (non-mine and non-0)
                self.update_point(row=neighbor_point.get_row(), column=neighbor_point.get_column(), visible=True)

    def player_won(self):
        return self.is_game_over()

    def is_game_over(self):
        for row in self._grid:
            for point in row:
                if (not point.is_visible()) and point.get_value != Minesweeper.MINE:
                    return False
        return True

    def play(self):
        while True:
            self.player_turn()
            if self.is_game_over():
                break

def main():
    m = Minesweeper(level='easy')
    m.play()

if __name__ == '__main__':
    main()
