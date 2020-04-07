#!/usr/bin/env python3
import signal
import numpy as np
from blessed import Terminal
from .figlet_digits import get_digit
from .arg_parser import parser
from .board import Board
from .modals import show_help, show_victory
from .puzzles import get_puzzle

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
board_grid = BLANK_BOARD.splitlines()

SMALL_BLANK_BOARD = """\
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │   ║   │   │   ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝"""
small_board_grid = SMALL_BLANK_BOARD.splitlines()


def draw_digit(cell, n, color_func=lambda x: x):
    i, j = cell
    if compact_view:
        u, v = 2 * i + 1 + vgap, 4 * j + 2 + hgap
        print(t.move(u, v) + color_func(str(n)))
    else:
        # get coords for top left of cell interior
        u, v = i * 4 + 1 + vgap, j * 8 + 1 + hgap

        digit = get_digit(FONT, n)
        for line_no, line in enumerate(digit):
            print(t.move(u + line_no, v) + color_func(line))


def highlight_cell(cell, color_func):
    i, j = cell
    if compact_view:
        # coords for top left of square
        u, v = i * 2, j * 4
        # top
        s = small_board_grid[u][v + 1 : v + 4]
        print(t.move(u + vgap, v + 1 + hgap) + color_func(s))
        # sides
        left = small_board_grid[u + 1][v]
        print(t.move(u + 1 + vgap, v + hgap) + color_func(left))
        right = small_board_grid[u + 1][v + 4]
        print(t.move(u + 1 + vgap, v + 4 + hgap) + color_func(right))
        # bottom
        s = small_board_grid[u + 2][v + 1 : v + 4]
        print(t.move(u + 2 + vgap, v + 1 + hgap) + color_func(s))
    else:
        # relative coords for top left of cell border
        u, v = i * 4, j * 8
        # top
        s = board_grid[u][v + 1 : v + 8]
        print(t.move(u + vgap, v + 1 + hgap) + color_func(s))
        # bottom
        s = board_grid[u + 4][v + 1 : v + 8]
        print(t.move(u + 4 + vgap, v + 1 + hgap) + color_func(s), end="")
        # sides
        for x in range(1, 4):
            left = board_grid[u + x][v]
            print(t.move(u + x + vgap, v + hgap) + color_func(left))
            right = board_grid[u + x][v + 8]
            print(t.move(u + x + vgap, v + 8 + hgap) + color_func(right))


def draw_cell_notes(cell, nums):
    i, j = cell
    # get coords for top left of cell interior
    u, v = i * 4 + 1 + vgap, j * 8 + 2 + hgap

    for n in range(0, 9):
        if n + 1 in nums:
            print(t.move(u + n // 3, v + 2 * (n % 3)) + str(n + 1))


def draw_all_notes(cursor_cell, drawn_cells):
    if compact_view:
        nums = b.get_note(cursor_cell)
        status = "Notes:  "
        for i in range(1, 10):
            if i in nums:
                status += t.green(str(i)) + "  "
            else:
                status += t.bright_black(str(i)) + "  "
        print(t.move(19 + vgap + min(vgap, 2), 2 + hgap) + status, end="")
    else:
        for cell, note in b.get_all_notes().items():
            if cell not in drawn_cells:
                draw_cell_notes(cell, note)


def draw(*cursor_cell):
    print(t.clear)
    if t.height < 21 or t.width < 37:
        print(t.home + "Please resize terminal to at least 37x21")
        return

    drawn_cells = set()
    bad_cells = b.check()

    # draw the grid
    for line_no, line in enumerate(small_board_grid if compact_view else board_grid):
        print(t.move(line_no + vgap, hgap) + line, end="")

    # draw the numbers that were given by the puzzle
    for cell, n in b.puzzle_entries.items():
        drawn_cells.add(cell)
        if cell in bad_cells:
            draw_digit(cell, n, color_func=t.bold_bright_red)
        else:
            draw_digit(cell, n, color_func=t.blue)

    # draw the numbers added by the user
    for cell, n in b.player_entries.items():
        drawn_cells.add(cell)
        if cell in bad_cells:
            draw_digit(cell, n, color_func=t.bold_bright_red)
        else:
            draw_digit(cell, n)

    draw_all_notes(cursor_cell, drawn_cells)

    # highlight cells with same value
    target = b[cursor_cell]
    [highlight_cell(c, t.magenta) for c in b.get_all_same(target)]

    # highlight selected cell
    highlight_cell(cursor_cell, t.green if notes_mode else t.yellow)

    # draw status bar
    if notes_mode:
        print(t.home + t.green("-- notes mode --  (space to cancel)"))


def on_resize(*args):
    global hgap, vgap, compact_view
    if t.width < 73 or t.height < 38 or FORCE_COMPACT:
        compact_view = True
        hgap = (t.width - 37) // 2
        vgap = (t.height - 21) // 2 + 1
    else:
        compact_view = False
        hgap = (t.width - 73) // 2
        vgap = (t.height - 37) // 2 + 1
    # tee hee let's just stick a new field on the terminal
    t.resized = True


def main():
    global t, b, FORCE_COMPACT, FONT, notes_mode

    args = parser.parse_args()
    FONT = args.font
    FORCE_COMPACT = args.force_compact

    if args.puzzle:
        PUZZLE_STRING = args.puzzle
    else:
        PUZZLE_STRING = get_puzzle(args.difficulty)

    t = Terminal()

    signal.signal(signal.SIGWINCH, on_resize)

    b = Board(PUZZLE_STRING)

    with t.fullscreen(), t.hidden_cursor(), t.cbreak():
        on_resize()
        notes_mode = False
        i, j = 0, 0
        draw(i, j)
        while (val := t.inkey(esc_delay=0, timeout=0.5)) != "q":
            if val == "":
                if not t.resized:
                    continue
            elif val == "k" or val.name == "KEY_UP":
                if (i := i - 1) < 0:
                    i = 0
                    continue
            elif val == "j" or val.name == "KEY_DOWN":
                if (i := i + 1) > 8:
                    i = 8
                    continue
            elif val == "h" or val.name == "KEY_LEFT":
                if (j := j - 1) < 0:
                    j = 0
                    continue
            elif val == "l" or val.name == "KEY_RIGHT":
                if (j := j + 1) > 8:
                    j = 8
                    continue
            elif val == " ":
                notes_mode = not notes_mode
            elif val.name == "KEY_ESCAPE":
                notes_mode = False
            elif val in "0123456789":
                if notes_mode:
                    b.make_note((i, j), int(val))
                else:
                    b[i, j] = int(val)
            elif val == "x":
                b[i, j] = 0
            elif val in "?H":
                show_help(t, lambda: draw(i, j))

            draw(i, j)
            t.resized = False

            if b.is_solved():
                show_victory(t, lambda: draw(i, j))
                break
