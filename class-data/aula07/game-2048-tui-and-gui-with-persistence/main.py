import os.path

import game
import tui_mode
import gui_mode


if __name__ == '__main__':
    board = None

    if os.path.exists('board.txt'):
        answer = 'invalid'
        while answer not in ('y', 'n', ''):
            answer = input('Reload the last game? [Y/n]').lower()

        if answer in ('y', ''):
            board = game.load_board('board.txt')

    if board is None:
        board = game.create_board(4, 4)

    mode = ''
    while mode not in ('tui', 'gui'):
        mode = input('TUI or GUI mode? ').lower()

    if mode == 'tui':
        board = tui_mode.run(board)
    else:
        board = gui_mode.run(board)

    game.save_board(board, 'board.txt')
