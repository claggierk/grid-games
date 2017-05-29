from random import randint
import itertools
import sys
sys.path.insert(0, "/Users/clark/projects/grid_games")

from grid.grid import Grid
from grid.point import Point, PointXY

class BattleShip(Grid):
    BOATS_LENGTHS = [2, 3, 4, 5, 6]
    BOAT_NAMES = [
        "Patrol Boat",      # 2
        "Submarine",        # 3
        "Destroyer",        # 4
        "Battleship",       # 5
        "Aircraft Carrier", # 6
    ]

    def __init__(self, num_rows, num_columns):
        super(BattleShip, self).__init__(num_rows, num_columns)
        self._boats = self._get_boats()
        self._add_boats_to_grid()

    def _add_boats_to_grid(self):
        for boat in self._boats:
            for boat_point in boat:
                self.set_point(boat_point)

    def _get_boats(self):
        all_boats = []
        for boat_length, boat_name in zip(BattleShip.BOATS_LENGTHS, BattleShip.BOAT_NAMES):

            while True:
                # orientation = vertical or horizontal
                orientation = randint(0, 1)
                boat_points = []
                boat_number = str(boat_length)

                # vertical
                if orientation:
                    max_row_index = self._num_rows - boat_length
                    max_column_index = self._num_columns - 1
                    start_row_index = randint(0, max_row_index)
                    start_column_index = randint(0, max_column_index)

                    for boat_row_index in range(start_row_index, start_row_index + boat_length, 1):
                        boat_points.append(Point(row=boat_row_index, column=start_column_index, value=boat_number, group=boat_name))

                # horizontal
                else:
                    max_row_index = self._num_rows - 1
                    max_column_index = self._num_columns - boat_length
                    start_row_index = randint(0, max_row_index)
                    start_column_index = randint(0, max_column_index)

                    for boat_column_index in range(start_column_index, start_column_index + boat_length, 1):
                        boat_points.append(Point(row=start_row_index, column=boat_column_index, value=boat_number, group=boat_name))

                # determine if ANY of the current proposed boat's points are
                # already part of another boat!
                proposed_boat_pointsxy = set([PointXY(p.get_row(), p.get_column()) for p in boat_points])
                all_boats_pointsxy = set([PointXY(p.get_row(), p.get_column()) for p in list(itertools.chain(*all_boats))])
                if set.intersection(proposed_boat_pointsxy, all_boats_pointsxy):
                    print " ##### Proposed boat intersected some other boat... generating new boat"
                else:
                    # there is no intersection between the proposed boat append
                    # all the other boats, therefore, the proposed boat is good!
                    all_boats.append(boat_points)
                    print "Random boat generated:", all_boats[-1]
                    break

        return all_boats

    def _boat_sunk(self, boat_name):
        boat_points = self.get_group_points(boat_name)
        print boat_points
        for boat_point in boat_points:
            if not boat_point.get_visible():
                return False
        return True

    def player_turn(self):
        while True:
            user_point = self.get_user_point()
            if not self.is_point_visible(user_point):
                break
            print "Invalid guess; Please provide a valid point."

        if self.is_point_valueless(user_point):
            print " ***** MISS ..."
            self.update_point(user_point.get_row(), user_point.get_column(), value='X', visible=True)
        else:
            self.illuminate_point(user_point)
            boat_name = self.get_point(user_point).get_group()
            if self._boat_sunk(boat_name):
                print " ***** Battleship Sunk: {} !!!".format(boat_name)
            else:
                print " ***** HIT {} !!!".format(boat_name)

    def is_game_over(self):
        if self.no_turns_left():
            print " ### No turns left!"
            return True

        # go through all the boat points
        for boat_points in self._boats:
            for boat_point in boat_points:
                # if one boat point is invisible, then its not sunk
                if not self.get_point(boat_point).get_visible():
                    return False

        print "Player wins!"
        print self.output(show_indicies=True, hide_invisible=True)
        return True

    def no_turns_left(self):
        # NA --- if there are 0 turns left to play, they would have won!
        pass

    def play(self):
        while True:
            print self.output(show_indicies=True)
            print self.output(show_indicies=True, hide_invisible=True)
            self.player_turn()
            if self.is_game_over():
                break

def main():
    battleship = BattleShip(num_rows=10, num_columns=10)
    battleship.play()

if __name__ == '__main__':
    main()
