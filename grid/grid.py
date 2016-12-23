from point import Point
from game import Game

class Grid(Game):
    def __init__(self, num_rows, num_columns):
        try:
            if int(num_rows) < 2:
                num_rows = 2
            elif num_rows > 99:
                num_rows = 99
            self._num_rows = num_rows

            if int(num_columns) < 2:
                num_columns = 2
            elif num_columns > 99:
                num_rows = 99
            self._num_columns = num_columns
        except Exception as e:
            self._num_rows = 10
            self._num_columns = 10

        self._grid = self._create_grid()

    def _create_grid(self):
        grid = []
        for row_index in range(self._num_rows):
            grid.append([])
            for column_index in range(self._num_columns):
                grid[-1].append(
                    Point(row_index, column_index, None)
                )
        return grid

    def is_point_valueless(self, my_point):
        if self.get_point(my_point).get_value():
            return False
        else:
            return True

    def is_point_visible(self, my_point):
        if self.get_point(my_point).get_visible():
            return True
        else:
            return False

    def get_invisible_points(self):
        invisible_points = []
        for row in self._grid:
            for point in row:
                if not point.get_visible:
                    invisible_points.append(point)
        return invisible_points

    def get_vertical_points(self, column=0):
        vertical_points = [row[column] for row in self._grid]
        return [point for point in reversed(vertical_points)]

    def get_horizontal_points(self, row=0):
        return self._grid[row]

    def get_empty_points(self):
        empty_points = []
        for row in self._grid:
            for point in row:
                if not point.get_value():
                    empty_points.append(point)
        return empty_points

    def output(self, show_column_indicies=False, show_row_indicies=False, show_indicies=False, hide_invisible=False):
        # deal with the top indices line
        if show_column_indicies or show_indicies:
            if len(self._grid) > 9:
                one_to_nine = '  '.join([str(num+1) for num in range(9)])
                ten_forward = ' '.join([str(num+1) for num in range(9, self._num_columns)])
                grid_string = ['   ' + one_to_nine + ' ' + ten_forward]
            else:
                grid_string = ['   ' + '  '.join([str(num+1) for num in range(self._num_columns)])]
        else:
            grid_string = []

        # the grid
        for row_index, row in enumerate(self._grid):
            if hide_invisible:
                row_values = map(lambda x: x.get_value() if x.get_value() and x.get_visible() else '.', row)
            else:
                row_values = map(lambda x: x.get_value() if x.get_value() else '.', row)
            if show_row_indicies or show_indicies:
                add_space = ''
                if len(str(row_index+1)) == 1:
                    add_space = ' '
                grid_string.append(add_space + str(row_index+1) + ' ' + '  '.join(row_values))
            elif show_column_indicies:
                grid_string.append('   ' + '  '.join(row_values))
            else:
                grid_string.append(' '.join(row_values))

        return '\n' + '\n'.join(grid_string) + '\n'

    def __repr__(self):
        return self.output()

    def get_point(self, my_point):
        return self._grid[my_point.get_row()][my_point.get_column()]

    def get_points(self, my_points):
        return [self.get_point(my_point) for my_point in my_points]

    def get_user_input(self, ask_row=True, ask_column=True, ask_value=False):
        row = None
        column = None
        value = None

        while True:
            try:
                if ask_row:
                    row = int(raw_input("Row    #: "))
                if ask_column:
                    column = int(raw_input("Column #: "))
                if ask_value:
                    value = raw_input("Value   : ")
                    if len(value) != 1:
                        continue
            except Exception as e:
                continue

            # obtained valid input
            break

        if row and column:
            return Point(row=row-1, column=column-1, value=value)
        elif row:
            return row
        elif column:
            return column

    def set_point(self, my_point):
        self._grid[my_point.get_row()][my_point.get_column()] = my_point

    def illuminate_point(self, my_point):
        self._grid[my_point.get_row()][my_point.get_column()].set_visible(True)

    def update_point(self, row, column, value=None, visible=None):
        if value is not None:
            self._grid[row][column].set_value(value)
        if visible is not None:
            self._grid[row][column].set_visible(visible)

    def get_value(self, x, y):
        return self._grid[x][y].get_value()

    def get_group_points(self, group_name):
        group_points = []
        for row in self._grid:
            for point in row:
                if point.get_group() == group_name:
                    group_points.append(point)
        return group_points

def main():
    g = Grid(num_rows=10, num_columns=10)
    print g.output(show_indicies=True)

if __name__ == '__main__':
    main()
