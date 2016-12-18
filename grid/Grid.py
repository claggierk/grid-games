from Point import Point

class MetaGrid(type):
    pass

class Grid(object):
    __metaclass__ = MetaGrid

    def __init__(self, num_rows, num_columns):
        if num_rows > 99:
            num_rows = 99
        if num_columns > 99:
            num_rows = 99
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._grid = self._create_grid()

    def _create_grid(self, initial_cell_value='.'):
        grid = []
        for row_index in range(self._num_rows):
            grid.append([])
            for column_index in range(self._num_columns):
                grid[-1].append(
                    Point(row_index, column_index, initial_cell_value)
                )
        return grid

    def get_vertical_points(self, column=0):
        vertical_points = [row_points[column] for row_points in self._grid]
        return vertical_points
        # return [row_points[x] for row_points in self._grid]

    def get_horizontal_points(self, row=0):
        return self._grid[row]

    def output(self, show_indicies=False):
        if show_indicies:
            if len(self._grid) > 9:
                one_to_nine = '  '.join([str(num+1) for num in range(9)])
                ten_forward = ' '.join([str(num+1) for num in range(9, len(self._grid))])
                grid_string = ['   ' + one_to_nine + ' ' + ten_forward]
            else:
                grid_string = ['   ' + '  '.join([str(num+1) for num in range(len(self._grid))])]
        else:
            grid_string = []
        for row_index, row in enumerate(self._grid):
            row_values = map(lambda x: x.get_value() if x.get_value() else ' ', row)
            if show_indicies:
                add_space = ''
                if len(str(row_index+1)) == 1:
                    add_space = ' '
                grid_string.append(add_space + str(row_index+1) + ' ' + '  '.join(row_values))
            else:
                grid_string.append(' '.join(row_values))
        return '\n'.join(grid_string) + '\n'

    def __repr__(self):
        return self.output()

    def set_user_point(self, ask_value=True):
        while True:
            try:
                row = int(raw_input("Row    #: "))
                column = int(raw_input("Column #:"))
                if ask_value:
                    value = raw_input("Value   :")
                    if len(value) != 1:
                        continue
                break
            except Exception as e:
                continue

            self.set_point(Point(row=row, column=column))

    def update_point(self, row, column, value=None):
        if value:
            self.self._grid[my_point.get_x()][my_point.get_y()].set_value(value)

    def set_point(self, my_point):
        self._grid[my_point.get_x()][my_point.get_y()] = my_point

    def get_point(self, my_point):
        return self._grid[my_point.get_x()][my_point.get_y()]

    def get_value(self, x, y):
        return self._grid[x][y].get_value()

def main():
    g = Grid(num_rows=10, num_columns=10)
    print g.output(show_indicies=True)
    print g.get_vertical_points(4)

if __name__ == '__main__':
    main()
