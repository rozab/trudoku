#!/usr/bin/env python3
import signal
from collections import namedtuple
import numpy as np
from blessed import Terminal
from figlet_digits import get_digit

BLANK_BOARD = """\
╔═══════╤═══════╤═══════╦═══════╤═══════╤═══════╦═══════╤═══════╤═══════╗
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╠═══════╪═══════╪═══════╬═══════╪═══════╪═══════╬═══════╪═══════╪═══════╣
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╠═══════╪═══════╪═══════╬═══════╪═══════╪═══════╬═══════╪═══════╪═══════╣
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
║       │       │       ║       │       │       ║       │       │       ║
╚═══════╧═══════╧═══════╩═══════╧═══════╧═══════╩═══════╧═══════╧═══════╝"""

# Lists of lists of tuples, containing coords of cells to check in each group
ROW_GROUPS = [[(i, j) for j in range(9)] for i in range(9)]
COLUMN_GROUPS = [[(i, j) for i in range(9)] for j in range(9)]
BOX_GROUPS = [
    [(i * 3 + u, j * 3 + v) for u in range(3) for v in range(3)] for i in range(3) for j in range(3)
]
ALL_GROUPS = ROW_GROUPS + COLUMN_GROUPS + BOX_GROUPS

PUZZLE = "002000500010705020400090007049000730801030409036000210200080004080902060007000800"
FONT = "straight"


def set_cell(n, i, j):
    if not puzzle_array[i, j]:
        # update array
        board_array[i, j] = n
        # update dict
        if n == 0:
            del player_entries[(i, j)]
        else:
            player_entries[(i, j)] = n


def check():
    bad_cells = set()
    for group in ALL_GROUPS:
        group_values = set()
        repeated_values = set()
        for cell in group:
            n = board_array[cell]
            if n == 0:
                continue
            elif n not in group_values:
                group_values.add(n)
            else:
                repeated_values.add(n)
        for cell in group:
            n = board_array[cell]
            if n in repeated_values:
                bad_cells.add(cell)
    return bad_cells


def draw_digit(i, j, n, color_func=lambda x: x):
    global hgap, vgap
    digit = get_digit(FONT, n)
    for line_no, line in enumerate(digit):
        print(t.move(i * 4 + 1 + vgap + line_no, j * 8 + 1 + hgap) + color_func(line))


def highlight_cell(i, j, color_func):
    global hgap, vgap
    # coords for top left of cell border
    u, v = i * 4, j * 8
    # top
    s = board_grid[u][v + 1 : v + 8]
    print(t.move(u + vgap, v + 1 + hgap) + color_func(s))
    # bottom
    s = board_grid[u + 4][v + 1 : v + 8]
    print(t.move(u + 4 + vgap, v + 1 + hgap) + color_func(s))
    # sides
    for x in range(1, 4):
        left = board_grid[u + x][v]
        print(t.move(u + x + vgap, v + hgap) + color_func(left))
        right = board_grid[u + x][v + 8]
        print(t.move(u + x + vgap, v + 8 + hgap) + color_func(right))


def draw(cursor_i, cursor_j):
    global hgap, vgap
    drawn_cells = set()
    bad_cells = check()
    t.clear()

    # draw the grid
    for line_no, line in enumerate(board_grid):
        print(t.move(line_no + vgap, hgap) + line)

    # draw the numbers that were given by the puzzle
    for (i, j), n in puzzle_entries.items():
        drawn_cells.add((i, j))
        if (i, j) in bad_cells:
            draw_digit(i, j, n, color_func=t.bold_red)
        else:
            draw_digit(i, j, n, color_func=t.blue)

    # draw the numbers added by the user
    for (i, j), n in player_entries.items():
        drawn_cells.add((i, j))
        if (i, j) in bad_cells:
            draw_digit(i, j, n, color_func=t.bold_red)
        else:
            draw_digit(i, j, n)

    # highlight selected cell
    highlight_cell(cursor_i, cursor_j, t.yellow)

    # highlight other cells with same value
    target = board_array[cursor_i, cursor_j]
    if target:
        cells = np.argwhere(board_array == target)
        with t.location(0, 0):
            print(cells)
        for cell in cells:
            if (i, j) != tuple(cell):
                highlight_cell(*cell, t.magenta)


def move_cursor(val, i, j):
    if val == "k" or val.name == "KEY_UP":
        i = max(i - 1, 0)
    elif val == "j" or val.name == "KEY_DOWN":
        i = min(i + 1, 8)
    elif val == "h" or val.name == "KEY_LEFT":
        j = max(j - 1, 0)
    elif val == "l" or val.name == "KEY_RIGHT":
        j = min(j + 1, 8)
    return i, j


t = Terminal()

puzzle_array = np.fromiter(PUZZLE, dtype=int).reshape([9, 9]).T
board_array = puzzle_array.copy()

board_grid = BLANK_BOARD.splitlines()

puzzle_entries = {}
player_entries = {}
for i in range(9):
    for j in range(9):
        n = puzzle_array[i][j]
        if n != 0:
            puzzle_entries[(i, j)] = n

with t.fullscreen(), t.hidden_cursor(), t.cbreak():
    hgap = (t.width - 73) // 2
    vgap = (t.height - 37) // 2
    i, j = 0, 0
    val = ""
    while val != "q":
        draw(i, j)
        val = t.inkey()

        if val == "k" or val.name == "KEY_UP":
            i = max(i - 1, 0)
        elif val == "j" or val.name == "KEY_DOWN":
            i = min(i + 1, 8)
        elif val == "h" or val.name == "KEY_LEFT":
            j = max(j - 1, 0)
        elif val == "l" or val.name == "KEY_RIGHT":
            j = min(j + 1, 8)
        elif val in "0123456789":
            set_cell(int(val), i, j)
        elif val == "x":
            set_cell(0, i, j)