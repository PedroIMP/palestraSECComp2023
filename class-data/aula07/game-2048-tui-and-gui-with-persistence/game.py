"""
Module responsible for the game logic.
"""
import random


def create_board(num_rows, num_columns):
    # Create an empty board
    board = []
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            row.append(0)
        board.append(row)

    create_new_cell(board)

    return board


def save_board(board, path):
    with open(path, 'w') as f:
        for row in board:
            line = ' '.join(str(n) for n in row)
            print(line, file=f)


def load_board(path):
    board = []

    with open(path, 'r') as f:
        for line in f:
            row = [int(n) for n in line.strip().split()]
            board.append(row)

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

    # Move cells to the left
    for row in board:
        new_row = [0] * len(row)
        head = 0
        candidate = False
        for n in row:
            if n == 0:
                continue

            if candidate:
                # Sum the two values if n equals the previous value
                if new_row[head - 1] == n:
                    new_row[head - 1] += n
                    candidate = False
                else:
                    new_row[head] = n
                    head += 1
            else:
                candidate = True
                new_row[head] = n
                head += 1

        new_board.append(new_row)

    if new_board == board:
        return None

    # Create a new cell
    create_new_cell(new_board)

    return new_board


def react_right(board):
    # Reverse the rows
    new_board = [
        list(reversed(row)) for row in board
    ]

    new_board = react_left(new_board)

    if new_board is None:
        return None

    # Reverse the rows back to the original orientation
    new_board = [
        list(reversed(row)) for row in new_board
    ]

    return new_board


def react_up(board):
    new_board = transpose(board)
    new_board = react_left(new_board)

    if new_board is None:
        return None

    new_board = transpose(new_board)
    return new_board


def react_down(board):
    new_board = transpose(board)
    new_board = react_right(new_board)

    if new_board is None:
        return None

    new_board = transpose(new_board)
    return new_board


def transpose(board):
    num_rows = len(board)
    num_columns = len(board[0])

    new_board = [[0] * num_rows for j in range(num_columns)]

    # Do the transpose
    for i in range(num_rows):
        for j in range(num_columns):
            new_board[j][i] = board[i][j]

    return new_board

def create_new_cell(board):
    num_rows = len(board)
    num_columns = len(board[0])

    empty_positions = []
    for i in range(num_rows):
        for j in range(num_columns):
            if board[i][j] == 0:
                empty_positions.append((i, j))

    if empty_positions:
        i, j = random.choice(empty_positions)
        board[i][j] = 2
