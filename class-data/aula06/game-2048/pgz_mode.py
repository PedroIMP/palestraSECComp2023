import math
import sys

import pygame
import pgzero.runner

import game


WIDTH = 400
HEIGHT = 400

BLOCK_WIDTH = 100
BLOCK_HEIGHT = 100

BACKGROUND_COLOR = 221, 224, 210

H_PADDING = int(.1 * BLOCK_WIDTH)
V_PADDING = int(.1 * BLOCK_HEIGHT)

COLORS = [pygame.Color(0) for _ in range(12)]
for i, c in enumerate(COLORS):
    COLORS[i].hsla = (
        245 - 245 / 11 * i,
        40 + 50 / 11 * i,
        60 - 20 / 11 * i,
        100,
    )


board = game.create_board(4, 4)


def draw():
    screen.fill(BACKGROUND_COLOR)

    for i, row in enumerate(board):
        for j, n in enumerate(row):
            x = j * BLOCK_WIDTH
            y = i * BLOCK_HEIGHT

            if n:
                color = COLORS[int(math.log2(n)) % len(COLORS)]
                block_rect = Rect(
                    (x, y),
                    (BLOCK_WIDTH, BLOCK_HEIGHT),
                )
                screen.draw.filled_rect(block_rect, color)

                text_rect = Rect(
                    (x + H_PADDING, y + V_PADDING),
                    (BLOCK_WIDTH - 2*H_PADDING, BLOCK_HEIGHT - 2 * V_PADDING)
                )
                text = str(n)
                screen.draw.textbox(str(n), text_rect)


def on_key_down(key):
    global board
    key_to_action_map = {
        keys.LEFT: 'LEFT',
        keys.RIGHT: 'RIGHT',
        keys.UP: 'UP',
        keys.DOWN: 'DOWN',
    }
    action = key_to_action_map.get(key)
    new_board = game.react(board, action)
    if new_board:
        board = new_board


def run():
    mod = sys.modules[__name__]
    pgzero.runner.prepare_mod(mod)
    pgzero.runner.run_mod(mod)


if __name__ == '__main__':
    run()
