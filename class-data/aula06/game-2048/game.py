import random


NUM_ROWS = 4
NUM_COLUMNS = 4

def create_board(num_rows, num_columns):
    board = [[0] * NUM_COLUMNS for _ in range(num_rows)]

    i = random.randint(0, num_rows - 1)
    j = random.randint(0, num_columns - 1)
    board[i][j] = 2

    return board


def react(board, action):
    if action == 'LEFT':
        return react_left(board)
    elif action == 'RIGHT':
        return react_right(board)
    elif action == 'UP':
        return react_up(board)
    elif action == 'DOWN':
        return react_down(board)

    return None


def react_left(board):
    new_board = []
    for row in board:
        new_row = [0] * len(row)
        head = 0
        is_candidate = False
        for value in row:
            if not value:
                continue
            if is_candidate and new_row[head - 1] == value:
                new_row[head - 1] *= 2
                is_candidate = False
            else:
                new_row[head] = value
                head += 1
                is_candidate = True
        new_board.append(new_row)

    if new_board == board:
        return None

    positions_left = []
    for i, row in enumerate(new_board):
        for j, value in enumerate(row):
            if not value:
                positions_left.append((i, j))

    if positions_left:
        idx = random.randint(0, len(positions_left) - 1)
        i, j = positions_left[idx]
        new_board[i][j] = 2

    return new_board


def react_right(board):
    board = [list(reversed(row)) for row in board]
    new_board = react_left(board)
    if new_board:
        new_board = [list(reversed(row)) for row in new_board]
    return new_board


def transpose(board):
    num_rows = len(board)
    num_cols = len(board[0])
    new_board = [[0] * num_rows for _ in range(num_cols)]
    for i in range(num_rows):
        for j in range(num_cols):
            new_board[j][i] = board[i][j]
    return new_board


def react_up(board):
    board = transpose(board)
    new_board = react_left(board)
    if new_board:
        new_board = transpose(new_board)
    return new_board


def react_down(board):
    board = transpose(board)
    new_board = react_right(board)
    if new_board:
        new_board = transpose(new_board)
    return new_board
