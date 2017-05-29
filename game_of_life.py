from copy import deepcopy
import time
import sys
sys.path.insert(0, "/Users/clark/projects/grid_games")

from grid.grid import Grid
from grid.point import Point

class GameOfLife(Grid):
    NUM_NEIGHBORS = 8
    DEAD = '.'
    ALIVE = '+'

    def __init__(self, num_rows, num_columns):
        super(GameOfLife, self).__init__(num_rows, num_columns)

    def construct_glider(self):
        #     +
        # +   +
        #   + +
        glider_points = [
            Point(row=0, column=2, value=GameOfLife.ALIVE),
            Point(row=1, column=0, value=GameOfLife.ALIVE),
            Point(row=1, column=2, value=GameOfLife.ALIVE),
            Point(row=2, column=1, value=GameOfLife.ALIVE),
            Point(row=2, column=2, value=GameOfLife.ALIVE),
        ]

        for glider_point in glider_points:
            self.set_point(glider_point)

    def is_alive(self, point):
        return self.get_point(point).get_value() == GameOfLife.ALIVE

    def is_dead(self, point):
        return not self.is_alive(point)

    def num_live_neighbors(self, point):
        num_alive_neighbors = 0
        for neighbor in self.get_neigbors(point):
            if self.is_alive(neighbor):
                num_alive_neighbors += 1

        return num_alive_neighbors

    def num_dead_neighbors(self, point):
        return GameOfLife.NUM_NEIGHBORS - self.num_live_neighbors(point)

    def make_alive(self, point):
        point.set_value(GameOfLife.ALIVE)
        self.set_point(point)

    def make_dead(self, point):
        point.set_value(GameOfLife.DEAD)
        self.set_point(point)

    # Any live cell with fewer than two live neighbors dies (as if caused by under-population)
    # Any live cell with two or three live neighbors lives on to the next generation
    # Any live cell with more than three live neighbors dies (as if by over-population)
    # Any dead cell with exactly three live neighbors becomes a live cell (as if by reproduction)
    def tick(self):
        grid_copy = deepcopy(self)
        neighbors_grid_copy = deepcopy(self)

        for row_index, row in enumerate(self._grid):
            for col_index, _ in enumerate(row):
                point = Point(row=row_index, column=col_index)

                # check the copy for the number of live neighbors
                number_of_live_neighbors = grid_copy.num_live_neighbors(point)

                # set the neighbor copy to the number of neighbors
                num_neighbors_point = Point(row=row_index, column=col_index, value=str(number_of_live_neighbors))
                neighbors_grid_copy.set_point(num_neighbors_point)

                if self.is_alive(point):
                    if number_of_live_neighbors != 2 and number_of_live_neighbors != 3:
                        print "DEAD", point
                        self.make_dead(point)
                else:
                    if number_of_live_neighbors == 3:
                        print "ALIVE", point
                        self.make_alive(point)
        print self
        print neighbors_grid_copy

    def play(self):
        while True:
            time.sleep(0.2)
            self.tick()

def main():
    gol = GameOfLife(8, 8)
    gol.construct_glider()
    print gol
    gol.play()

main()
