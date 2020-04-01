#!/usr/bin/env python3
from blessed import Terminal
import numpy as np
import signal

BLANK_BOARD = "\
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗\
║   │   │   ║   │   │   ║   │   │   ║\
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\
║   │   │   ║   │   │   ║   │   │   ║\
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\
║   │   │   ║   │   │   ║   │   │   ║\
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\
║   │   │   ║   │   │   ║   │   │   ║\
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\
║   │   │   ║   │   │   ║   │   │   ║\
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\
║   │   │   ║   │   │   ║   │   │   ║\
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\
║   │   │   ║   │   │   ║   │   │   ║\
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\
║   │   │   ║   │   │   ║   │   │   ║\
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\
║   │   │   ║   │   │   ║   │   │   ║\
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝"

# Lists of lists of tuples, containing coords of cells to check in each group
ROW_GROUPS = [ [(i,j) for j in range(9)] for i in range(9)]
COLUMN_GROUPS = [ [(i,j) for i in range(9)] for j in range(9)]
BOX_GROUPS = [ [(i*3 + u,j*3 + v) for u in range(3) for v in range(3)] for i in range(3) for j in range(3)]
ALL_GROUPS = ROW_GROUPS + COLUMN_GROUPS + BOX_GROUPS

PUZZLE = "002000500010705020400090007049000730801030409036000210200080004080902060007000800"


def set_cell(n, i, j):
    if not puzzle_array[i, j]:
        # update array
        board_array[i,j] = n
        # update display
        s = str(n) if n != 0 else " "
        board_display[2*j + 1][4*i + 2] = s

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

def highlight_conflicts(board, bad_cells):
    for i, j in bad_cells:
        # override other styling
        val = str(board_array[i,j])
        board[2*j + 1][4*i + 2] = t.bold_red(val)

def show_cursor(board, i, j):
    # highlight current cell
    highlight_cell(board, t.yellow, i, j)
    # highlight other cells with same value
    target = board_array[j, i]
    if target:
        cells = np.argwhere(board_array==target)
        with t.location(0,0):
            print(cells)
        for cell in cells:
            if (j, i) != tuple(cell):
                highlight_cell(board, t.magenta, cell[1], cell[0])

def highlight_cell(board, color, i, j):
    # coords for top left of square
    u, v = i*2, j*4
    # top
    board[u][v+1] = color + board[u][v+1]
    board[u][v+3] += t.normal
    #sides
    board[u+1][v] = color(board[u+1][v])
    board[u+1][v+4] = color(board[u+1][v+4])
    # bottom
    board[u+2][v+1] = color + board[u+2][v+1]
    board[u+2][v+3] += t.normal

def draw(i,j):
    width, height = t.width, t.height
    hgap = (width - 37) // 2
    vgap = (height - 19) // 2
    colored_board = board_display.copy()
    highlight_conflicts(colored_board, check())
    show_cursor(colored_board, i, j)
    lines = ["".join(l) for l in colored_board]

    t.clear()
    for i, l in enumerate(lines):
        print(t.move(i+vgap, hgap) + l)

def move_cursor(val, i,j):
    if val == "k" or val.name == "KEY_UP":
        i = max(i-1, 0)
    elif val == "j" or val.name == "KEY_DOWN":
        i = min(i+1, 8)
    elif val == "h" or val.name == "KEY_LEFT":
        j = max(j-1, 0)
    elif val == "l" or val.name == "KEY_RIGHT":
        j = min(j+1, 8)
    return i, j


t = Terminal()

puzzle_array = np.fromiter(PUZZLE, dtype=int).reshape([9,9]).T
board_array = puzzle_array.copy()

board_display = np.fromiter(list(BLANK_BOARD), dtype="U16").reshape([19,37])

for i in range(9):
    for j in range(9):
        n = board_array[i][j]
        if n != 0: board_display[2*j + 1][4*i + 2] = t.blue(str(n))

with t.fullscreen(), t.hidden_cursor(), t.cbreak():
    i, j = 0, 0
    val = ""
    while val != 'q':
        draw(i, j)
        val = t.inkey()

        if val == "k" or val.name == "KEY_UP":
            i = max(i-1, 0)
        elif val == "j" or val.name == "KEY_DOWN":
            i = min(i+1, 8)
        elif val == "h" or val.name == "KEY_LEFT":
            j = max(j-1, 0)
        elif val == "l" or val.name == "KEY_RIGHT":
            j = min(j+1, 8)
        elif val in "0123456789":
            set_cell(int(val), j, i)
        elif val == "x":
            set_cell(0, j, i)