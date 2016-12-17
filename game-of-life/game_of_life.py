from copy import deepcopy
import time

DEAD = '-'
ALIVE = '+'
NUM_NEIGHBORS = 8

def create_board(length):
    board = []
    for row in range(length):
        board.append([])
        for cell in range(length):
            board[row].append('-')
    return board

def output_board(board):
    for row in board:
        row_string = ''
        for cell in row:
            row_string += cell
        print row_string
    print ''

def is_alive(board, cell):
    try:
        x = cell[0]
        y = cell[1]
        return True if board[y][x] == ALIVE else False
    except IndexError:
        print x, y, cell
        print board
        raise

def is_dead(board, cell):
    return not is_alive(board, cell)

def determine_neigbors(board, cell):
    length = len(board)
    x = cell[0]
    y = cell[1]

    x_minus = (x - 1) % length
    x_plus = (x + 1) % length
    y_minus = (y - 1) % length
    y_plus = (y + 1) % length

    neighbors = [
        (x_minus, y_minus),
        (x_minus, y),
        (x_minus, y_plus),
        (x, y_minus),
        (x, y_plus),
        (x_plus, y_minus),
        (x_plus, y),
        (x_plus, y_plus),
    ]

    return neighbors

def num_live_neighbors(board, cell):
    num_alive_neighbors = 0
    for neighbor in determine_neigbors(board, cell):
        if is_alive(board, neighbor):
            num_alive_neighbors += 1

    return num_alive_neighbors

def num_dead_neighbors(board, cell):
    return NUM_NEIGHBORS - num_live_neighbors(board, cell)

def make_alive(board, cell):
    x = cell[0]
    y = cell[1]
    board[y][x] = ALIVE

def make_dead(board, cell):
    x = cell[0]
    y = cell[1]
    board[y][x] = DEAD

def toggle_cell(board, cell):
    x = cell[0]
    y = cell[1]
    dead_or_alive = DEAD if board[y][x] == ALIVE else ALIVE
    board[y][x] = dead_or_alive

def toggle_cells(board, cells):
    for cell in cells:
        toggle_cell(board, cell)

    return board

# Any live cell with fewer than two live neighbors dies (as if caused by under-population)
# Any live cell with two or three live neighbors lives on to the next generation
# Any live cell with more than three live neighbors dies (as if by over-population)
# Any dead cell with exactly three live neighbors becomes a live cell (as if by reproduction)
def tick(board):
    new_board = deepcopy(board)
    neighbors_board = deepcopy(board)
    for row_index, row in enumerate(board):
        for cell_index, _ in enumerate(row):
            cell = (row_index, cell_index,)
            number_of_live_neighbors = num_live_neighbors(board, cell)
            neighbors_board[row_index][cell_index] = str(number_of_live_neighbors)
            if is_alive(board, cell):
                if number_of_live_neighbors != 2 and number_of_live_neighbors != 3:
                    print "DEAD"
                    make_dead(new_board, cell)
            else:
                if number_of_live_neighbors == 3:
                    print "ALIVE", cell
                    make_alive(new_board, cell)
    output_board(neighbors_board)

    return new_board

def construct_glider():
    game_board = create_board(20)
    toggle_these_cells = [(0, 2), (1, 0), (1, 2), (2, 1), (2, 2),]
    game_board = toggle_cells(game_board, toggle_these_cells)
    output_board(game_board)
    return game_board

def main():
    game_board = construct_glider()
    while True:
        game_board = tick(game_board)
        output_board(game_board)
        time.sleep(1)
main()
