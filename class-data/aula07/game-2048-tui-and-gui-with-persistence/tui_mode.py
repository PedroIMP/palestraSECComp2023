import math
import curses

import game


CELL_WIDTH = 5
CELL_HEIGHT = 3


def num_to_str(number):
    s = str(number) if number else ' '
    position = (CELL_WIDTH - len(s)) // 2
    return ' ' * position + s + ' ' * (CELL_WIDTH - position - len(s))


def row_to_str(row):
    return ' '.join(num_to_str(n) for n in row)


def draw_row(window, row):
    y_offset, x_offset = window.getyx()
    for j, n in enumerate(row):
        s = num_to_str(n)
        color = 0
        if n:
            idx = int(round(math.log2(n)))
            color = curses.color_pair(idx)

        # Fill cell
        for i in range(CELL_HEIGHT):
            y = y_offset + i
            x = x_offset + j * CELL_WIDTH
            window.addstr(y, x, ' ' * CELL_WIDTH, color)

        y = y_offset + CELL_HEIGHT // 2
        x = x_offset + j * CELL_WIDTH
        window.addstr(y, x, s, color)


def draw_board(window, board):
    for i, row in enumerate(board):
        window.move(i * CELL_HEIGHT, 0)
        draw_row(window, row)


def main(stdscr, board):
    curses.use_default_colors()
    for i in range(12):
        curses.init_pair(i + 1, 0, (curses.COLORS // 12) * (i + 1))

    key = ''

    key_to_action_map = {
        'KEY_LEFT': 'LEFT',
        'KEY_RIGHT': 'RIGHT',
        'KEY_UP': 'UP',
        'KEY_DOWN': 'DOWN',
    }

    try:
        while True:
            stdscr.erase()
            draw_board(stdscr, board)

            while True:
                key = stdscr.getkey()
                action = key_to_action_map.get(key)
                new_board = game.react(board, action)

                if new_board:
                    board = new_board
                    break
    except KeyboardInterrupt:
        return board


def run(board):
    return curses.wrapper(main, board)


if __name__ == '__main__':
    run()
