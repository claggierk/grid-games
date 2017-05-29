from Grid import Grid, MetaGrid
from Game import Game, MetaGame
from Point import Point

ZERO_TO_NINE_SET = set([str(num+1) for num in range(9)])

class MetaSudoku(MetaGrid, MetaGame):
    pass

class Sudoku(Grid, Game):
    __metaclass__ = MetaSudoku

    SQUARE_SIDE = 9
    MINI_SQUARE_SIDE = 3
    point_to_grid_3x3_index = {}
    grid_3x3_index_to_points = {}

    @staticmethod
    def initialize_class_attributes(output=False):
        # XY
        # 0          1          2
        # 00 01 02   03 04 05   06 07 08
        # 10 11 12   13 14 15   16 17 18
        # 20 21 22   23 24 25   26 27 28

        # 3          4          5
        # 30 31 32   33 34 35   36 37 38
        # 40 41 42   43 44 45   46 47 48
        # 50 51 52   53 54 55   56 57 58

        # 6          7          8
        # 60 61 62   63 64 65   66 67 68
        # 70 71 72   73 74 75   76 77 78
        # 80 81 82   83 84 85   86 87 88

        mini_square_index = 0

        # big grid 3 row
        for x1 in xrange(Sudoku.MINI_SQUARE_SIDE):
            row_cell_numbers = []

            mini_square_offset = x1 * Sudoku.MINI_SQUARE_SIDE
            # big grid 3 column
            for x2 in xrange(Sudoku.MINI_SQUARE_SIDE):
                x = (x1 * Sudoku.MINI_SQUARE_SIDE) + x2

                mini_square_index = mini_square_offset
                # mini grid 3 row
                for y1 in xrange(Sudoku.MINI_SQUARE_SIDE):

                    # mini grid 3 column
                    for y2 in xrange(Sudoku.MINI_SQUARE_SIDE):
                        y = (y1 * Sudoku.MINI_SQUARE_SIDE) + y2
                        # print "Cell={}, {} <---> Mini-Square={}".format(x, y, mini_square_index)

                        try:
                            Sudoku.point_to_grid_3x3_index[x][y] = mini_square_index
                        except KeyError:
                            Sudoku.point_to_grid_3x3_index[x] = {y: mini_square_index}

                        try:
                            Sudoku.grid_3x3_index_to_points[mini_square_index].append(Point(x, y),)
                        except KeyError:
                            Sudoku.grid_3x3_index_to_points[mini_square_index] = [Point(x, y)]
                    mini_square_index += 1

                mini_square_index += 1
        if output:
            print " Point to Grid #:"
            for x, cells in Sudoku.point_to_grid_3x3_index.iteritems():
                for y, grid in cells.iteritems():
                    print "    {},{} --> {}".format(x, y, grid)

            print ""
            print " Grid to Points:"
            for grid_index, points in Sudoku.grid_3x3_index_to_points.iteritems():
                print "    Grid {}".format(grid_index)
                for point in points:
                    print "       ", point

    def __init__(self):
        super(Sudoku, self).__init__(Sudoku.SQUARE_SIDE, Sudoku.SQUARE_SIDE)
        self._grid = self.initialize_game()

        Sudoku.initialize_class_attributes(output=True)

    def initialize_game(self):
        initial_grid = [
            [' ', ' ', ' ',    '3', '6', '7',    ' ', '9', '1'],
            [' ', ' ', '1',    ' ', '2', '8',    '6', '3', '5'],
            [' ', '8', ' ',    ' ', ' ', '9',    '4', ' ', ' '],

            [' ', ' ', '6',    '1', ' ', ' ',    '7', ' ', ' '],
            ['8', ' ', '5',    ' ', ' ', '3',    '1', '6', '4'],
            ['1', '2', '7',    ' ', ' ', ' ',    ' ', '5', '9'],

            [' ', '3', '8',    '9', ' ', '6',    ' ', ' ', ' '],
            [' ', '6', ' ',    ' ', ' ', '1',    '2', ' ', ' '],
            [' ', ' ', '4',    '7', ' ', ' ',    '9', ' ', ' '],
        ]

        initial_point_grid = []
        for list_index, my_list in enumerate(initial_grid):
            initial_point_grid.append([])
            for string_index, my_string in enumerate(my_list):
                modifiable = False if my_string.strip() else True
                initial_point_grid[-1].append(Point(list_index, string_index, my_string.strip(), modifiable))
        return initial_point_grid

    def _get_used_vertical_numbers(self, my_point):
        return set([point.get_value() for point in self.get_vertical_points(column=my_point.get_y()) if point.get_value().isdigit()])

    def _get_used_horizontal_numbers(self, my_point):
        return set([point.get_value() for point in self.get_horizontal_points(row=my_point.get_x()) if point.get_value().isdigit()])

    def _get_local_grid_numbers(self, my_point):
        grid_index = Sudoku.point_to_grid_3x3_index[my_point.get_x()][my_point.get_y()]
        # print grid_index
        grid_points = Sudoku.grid_3x3_index_to_points[grid_index]
        # print grid_points
        real_grid_points = [self.get_point(grid_point) for grid_point in grid_points]
        # print real_grid_points
        grid_numbers = set([grid_point.get_value() for grid_point in real_grid_points if grid_point.get_value().isdigit()])
        # print grid_numbers
        return grid_numbers

    def get_available_numbers(self, x, y):
        my_point = Point(x, y)
        used_vertical_numbers = self._get_used_vertical_numbers(my_point)
        print "used_vertical_numbers:", used_vertical_numbers
        used_horizonal_numbers = self._get_used_horizontal_numbers(my_point)
        print "used_horizonal_numbers:", used_horizonal_numbers
        used_local_grid_numbers = self._get_local_grid_numbers(my_point)
        print "used_local_grid_numbers:", used_local_grid_numbers

        used_numbers = set.union(used_vertical_numbers, used_horizonal_numbers, used_local_grid_numbers)
        available_numbers = ZERO_TO_NINE_SET.difference(used_numbers)
        print "available_numbers:", available_numbers
        print ""
        return available_numbers

    def get_points_with_no_options(self):
        no_option_points = []
        for row in self._grid:
            for point in row:
                # it is modifiable and it has no value
                if point.get_modifiable() and not point.get_value().strip():
                    available_numbers = self.get_available_numbers(point.get_x(), point.get_y())
                    if not available_numbers:
                        no_option_points.append(point)
        return no_option_points

    def _is_invalid_guess(self, my_point):
        # if this point is NOT blank, then return False
        if not self.get_point(my_point).get_value():
            return False

        used_vertical_numbers = self._get_used_vertical_numbers(my_point)
        print 'vertical:', used_vertical_numbers
        used_horizonal_numbers = self._get_used_horizontal_numbers(my_point)
        print 'horizontal:', used_horizonal_numbers
        used_local_grid_numbers = self._get_local_grid_numbers(my_point)
        print 'grid:', used_local_grid_numbers

        used_numbers = set.union(used_vertical_numbers, used_horizonal_numbers, used_local_grid_numbers)
        print 'used_numbers:', used_numbers
        available_numbers = ZERO_TO_NINE_SET.difference(used_numbers)
        print 'available_numbers:', available_numbers

        if my_point.get_value() in available_numbers:
            return False
        return True

    def _get_user_point(self):
        invalid_guess = True
        # while invalid_guess:
        # x = int(raw_input("X    ="))
        # y = int(raw_input("Y    ="))
        # value = int(raw_input("Value="))
        x = 0
        y = 0
        value = '3'
        my_point = Point(x, y, value)
        invalid_guess = self._is_invalid_guess(my_point)
        print "GUESS:", value
        if invalid_guess:
            print "GOOD GUESS"
        else:
            print "BAD GUESS"

        return my_point

    def player_turn(self):
        self._get_user_point()

    def is_game_over(self):
        for row in self._grid:
            for point in row:
                if not point.get_value().isdigit():
                    return False
        return True

    def __repr__(self):
        print tuple([p.get_value() for p in self.get_horizontal_points(y=8)])
        print len([p.get_value() for p in self.get_horizontal_points(y=8)])
        return \
            "             Column Index\n"\
            "     _0_1_2___3_4_5___6_7_8__\n"\
            "  0 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=0)]) +\
            "R 1 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=1)]) +\
            "o 2 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=2)]) +\
            "w   -------------------------\n"\
            "  3 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=3)]) +\
            "I 4 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' if p.get_value() else ' ' for p in self.get_horizontal_points(y=4)]) +\
            "n 5 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=5)]) +\
            "d   -------------------------\n"\
            "e 6 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=6)]) +\
            "x 7 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=7)]) +\
            "  8 | {} {} {} | {} {} {} | {} {} {} |\n".format(*[p.get_value() if p.get_value() else ' ' for p in self.get_horizontal_points(y=8)])

def main():
    s = Sudoku()
    print s
    s.player_turn()

if __name__ == '__main__':
    main()
