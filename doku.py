#!/usr/bin/env python3
import numpy as np

class colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'

class Board():
    BLANK_BOARD = """\
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

    def __init__(self):
        self.board = np.zeros([9,9], dtype=int)
        self.board_display = [list(l) for l in self.BLANK_BOARD.splitlines()]

    def set_cell(self, n, i, j):
        self.board[i][j] = n
        self.update_cell(n, i, j)
        #self.draw()

    def draw(self):
        hboard = self.highlighted_board(self.check())
        result = "\n".join(["".join(l) for l in hboard])
        print(result)

    def update_cell(self, n, i, j):
        s = str(n) if n != 0 else " "
        self.board_display[2*j + 1][4*i + 2] = s

    def highlighted_board(self, bad_cells):
        hboard = self.board_display.copy()
        # we must work right to left so our indices don't get fucked
        cells = sorted(bad_cells, key=lambda x: x[0], reverse=True)
        for i, j in cells:
            line = hboard[2*j + 1]
            hboard[2*j + 1] = line[:4*i+2] + [colors.BOLD+colors.RED + line[4*i+2] + colors.RESET] + line[4*i+3:]
        return hboard

    def check(self):
        bad_cells = set()
        bad_cells |= self.check_rows()
        bad_cells |= self.check_columns()
        bad_cells |= self.check_blocks()
        return bad_cells

    def check_rows(self):
        bad_cells = set()
        for i in range(9):
            row_values = set()
            bad_values = set()
            for j in range(9):
                n = self.board[i][j]
                if n == 0:
                    continue
                elif n not in row_values:
                    row_values.add(n)
                else:
                    bad_values.add(n)
            for j in range(9):
                n = self.board[i][j]
                if n in bad_values:
                    bad_cells.add((i, j))
        return bad_cells

    def check_columns(self):
        bad_cells = set()
        for i in range(9):
            column_values = set()
            bad_values = set()
            for j in range(9):
                n = self.board[j][i]
                if n == 0:
                    continue
                elif n not in column_values:
                    column_values.add(n)
                else:
                    bad_values.add(n)
            for j in range(9):
                n = self.board[j][i]
                if n in bad_values:
                    bad_cells.add((j, i))
        return bad_cells

    def check_blocks(self):
        bad_cells = set()
        for i in range(3):
            for j in range(3):
                block_values = set()
                bad_values = set()
                for u in range(3):
                    for v in range(3):
                        n = self.board[i*3 + u][j*3 + v]
                        if n == 0:
                            continue
                        elif n not in block_values:
                            block_values.add(n)
                        else:
                            bad_values.add(n)
                for u in range(3):
                    for v in range(3):
                        n = self.board[i*3 + u][j*3 + v]
                        if n in bad_values:
                            bad_cells.add((i*3 + u, j*3 + v))
        return bad_cells