from Point import Point

class MetaGrid(type):
    pass

class Grid(object):
    __metaclass__ = MetaGrid

    def __init__(self, num_rows, num_columns):
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

    def __repr__(self):
        grid_string = []
        for row in self._grid:
            row_values = map(lambda x: x.get_value() if x.get_value() else ' ', row)
            grid_string.append(" ".join(row_values))
        return "\n".join(grid_string) + "\n"

    def set_point(self, my_point):
        self._grid[my_point.get_x()][my_point.get_y()] = my_point

    def get_point(self, my_point):
        return self._grid[my_point.get_x()][my_point.get_y()]

    def get_value(self, x, y):
        return self._grid[x][y].get_value()

def main():
    g = Grid(9, 9)
    print g
    print g.get_vertical_points(4)

if __name__ == '__main__':
    main()
