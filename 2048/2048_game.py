import numpy as np
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP

def init_game():
    board = np.zeros((4, 4), dtype=int)
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_cells = list(zip(*np.where(board == 0)))
    if empty_cells:
        x, y = empty_cells[np.random.randint(len(empty_cells))]
        board[x, y] = 2 if np.random.random() < 0.5 else 4

def move(board, direction):
    if direction in (KEY_UP, KEY_DOWN):
        board = board.T
    moves = {KEY_LEFT: -1, KEY_RIGHT: 1, KEY_UP: -1, KEY_DOWN: 1}
    moved = False

    for row in range(4):
        if direction in (KEY_RIGHT, KEY_DOWN):
            tiles = board[row][::-1]
        else:
            tiles = board[row]

        non_zeros = tiles[tiles != 0]
        new_tiles = np.zeros_like(tiles)
        idx = 0

        while len(non_zeros) > 0:
            current_tile = non_zeros[0]
            non_zeros = np.delete(non_zeros, 0)

            if len(non_zeros) > 0 and current_tile == non_zeros[0]:
                new_tiles[idx] = current_tile * 2
                non_zeros = np.delete(non_zeros, 0)
            else:
                new_tiles[idx] = current_tile

            idx += 1

        if direction in (KEY_RIGHT, KEY_DOWN):
            new_tiles = new_tiles[::-1]

        moved = moved or not np.array_equal(tiles, new_tiles)
        board[row] = new_tiles

    if direction in (KEY_UP, KEY_DOWN):
        board = board.T

    return moved

def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)

    stdscr.nodelay(1)
    stdscr.timeout(100)
    stdscr.keypad(1)

    board = init_game()

    while True:
        stdscr.erase()
        stdscr.addstr(0, 0, "2048 Game - Use arrow keys to move, 'q' to quit")

        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if tile:
                    stdscr.addstr(i + 1, j * 7, str(tile), curses.color_pair(1))
                else:
                    stdscr.addstr(i + 1, j * 7, '.', curses.color_pair(2))

        key = stdscr.getch()
        if key == ord('q'):
            break

        if key in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
            moved = move(board, key)
            if moved:
                add_random_tile(board)
                if np.all(board):
                    stdscr.addstr(6, 0, "Game Over! Press 'q' to quit.")
                    stdscr.refresh()
                    while stdscr.getch() != ord('q'):
                        pass
                    break

curses.wrapper(main)


