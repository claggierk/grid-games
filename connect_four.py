from random import randint
import sys
sys.path.insert(0, "/Users/clark/projects/grid_games")

from grid.grid import Grid
from grid.point import Point

class ConnectFour(Grid):
    NUM_ROWS = 6
    NUM_COLUMNS = 7

    def __init__(self):
        super(ConnectFour, self).__init__(ConnectFour.NUM_ROWS, ConnectFour.NUM_COLUMNS)

    def player_turn(self):
        # increment by 1 to align this with the user's guesses
        available_user_columns = [column+1 for column in self.get_available_columns()]
        while True:
            user_column = self.get_user_input(ask_row=False, ask_column=True)
            if user_column in available_user_columns:
                break
            print "Invalid guess; Please provide valid input."

        # decrement by 1 to align it with the legitimate grid
        user_column -= 1

        user_point = self.get_lowest_empty_point_in_column(column_index=user_column)
        user_point.set_value('X')
        self.set_point(user_point)

        return user_point

    def get_available_columns(self):
        available_columns = []
        for column_index in range(self._num_columns):
            vertical_points = self.get_vertical_points(column=column_index)
            for vertical_point in vertical_points:
                if not vertical_point.get_value():
                    available_columns.append(column_index)
                    break
        return available_columns

    def get_lowest_empty_point_in_column(self, column_index):
        vertical_points = self.get_vertical_points(column=column_index)
        for vertical_point in vertical_points:
            if not vertical_point.get_value():
                return vertical_point
        return None

    def computer_turn(self):
        available_columns = self.get_available_columns()
        random_index = randint(0, len(available_columns)-1)
        computer_column = available_columns[random_index]
        computer_point = self.get_lowest_empty_point_in_column(column_index=computer_column)
        computer_point.set_value('O')
        self.set_point(computer_point)
        return computer_point

    def is_game_over(self, turn_point):
        if self.player_won(turn_point):
            return True
        if self.no_turns_left():
            return True
        return False

    def no_turns_left(self):
        for row in self._grid:
            for point in row:
                if not point.get_value():
                    return False
        print self
        print " ***** NO TURNS LEFT *****"
        return True

    def get_horizontal_seven(self, turn_point):
        row = turn_point.get_row()
        column = turn_point.get_column()

        min_column_index = 0
        max_column_index = self._num_columns - 1

        left_index = row - 3
        right_index = row + 3

        if left_index < min_column_index:
            left_index = min_column_index
        if right_index > max_column_index:
            right_index = max_column_index

        row_points = self.get_horizontal_points(row=row)
        horizontal_seven = row_points[left_index:(right_index+1)]

        return horizontal_seven

    def get_vertical_seven(self, turn_point):
        row = turn_point.get_row()
        column = turn_point.get_column()

        min_row_index = 0
        max_row_index = self._num_rows - 1

        bottom_index = row - 3
        top_index = row + 3

        if bottom_index < min_row_index:
            bottom_index = min_row_index
        if top_index > max_row_index:
            top_index = max_row_index

        column_points = self.get_vertical_points(column=column)
        vertical_seven = column_points[bottom_index:(top_index+1)]

        return vertical_seven

    def get_diagonal_seven_positive(self, turn_point):
        row = turn_point.get_row()
        column = turn_point.get_column()

        min_row_index = 0
        max_row_index = self._num_rows - 1
        min_column_index = 0
        max_column_index = self._num_columns - 1
        #       ?
        #      ?
        #     ?
        #    X <-- turn_point
        #   ?
        #  ?
        # ?
        # bottom left
        current_row = row + 3
        current_column = column - 3

        diagonal_seven_positive = []
        for _ in range(7):
            if current_row < min_row_index or current_row > max_row_index or \
                current_column < min_column_index or current_column > max_column_index:
                pass # invalid point
            else:
                diagonal_seven_positive.append(self.get_point(Point(row=current_row, column=current_column)))

            current_row -= 1
            current_column += 1

        return diagonal_seven_positive

    def get_diagonal_seven_negative(self, turn_point):
        row = turn_point.get_row()
        column = turn_point.get_column()

        min_row_index = 0
        max_row_index = self._num_rows - 1
        min_column_index = 0
        max_column_index = self._num_columns - 1

        # ?
        #  ?
        #   ?
        #    X <-- turn_point
        #     ?
        #      ?
        #       ?
        # top left
        current_row = row - 3
        current_column = column - 3

        diagonal_seven_negative = []
        for _ in range(7):
            if current_row < min_row_index or current_row > max_row_index or \
                current_column < min_column_index or current_column > max_column_index:
                pass # invalid point
            else:
                diagonal_seven_negative.append(self.get_point(Point(row=current_row, column=current_column)))

            print "checking: {} {}".format(current_row, current_column)
            current_row += 1
            current_column += 1

        return diagonal_seven_negative

    def player_won(self, turn_point):
        check_linear_point_groups = []

        # horizontal_seven
        check_linear_point_groups.append(self.get_horizontal_seven(turn_point))

        # vertical_seven
        check_linear_point_groups.append(self.get_vertical_seven(turn_point))

        # diagonal_seven_positive
        check_linear_point_groups.append(self.get_diagonal_seven_positive(turn_point))

        # diagonal_seven_negative
        diagonal_seven_negative = self.get_diagonal_seven_negative(turn_point)
        print "diagonal_seven_negative:\n", diagonal_seven_negative
        check_linear_point_groups.append(diagonal_seven_negative)

        for check_linear_point_group in check_linear_point_groups:
            current_value = check_linear_point_group[0].get_value()
            winning_points = [check_linear_point_group[0]]
            for point in check_linear_point_group[1:]:
                if current_value and point.get_value() == current_value:
                    winning_points.append(point)
                    if len(winning_points) == 4:
                        print self
                        print " ***** PLAYER WON! *****"
                        print " Winning Points: ", winning_points
                        return True
                else:
                    current_value = point.get_value()
                    del winning_points[:]

        return False

    def play(self):
        while True:
            print self.output(show_column_indicies=True)
            player_turn_point = self.player_turn()
            if self.is_game_over(player_turn_point):
                break
            computer_turn_point = self.computer_turn()
            if self.is_game_over(computer_turn_point):
                break

def main():
    connect_four = ConnectFour()
    connect_four.play()

if __name__ == '__main__':
    main()
