from inspect import signature
import numpy as np

# Lists of lists of tuples, containing coords of cells to check in each group
ROW_GROUPS = [[(i, j) for j in range(9)] for i in range(9)]
COLUMN_GROUPS = [[(i, j) for i in range(9)] for j in range(9)]
BOX_GROUPS = [
    [(i * 3 + u, j * 3 + v) for u in range(3) for v in range(3)] for i in range(3) for j in range(3)
]
ALL_GROUPS = ROW_GROUPS + COLUMN_GROUPS + BOX_GROUPS


class Board:
    def __init__(self, puzzle_string):
        global dirty
        self.board_array = np.fromiter(puzzle_string, dtype=int).reshape([9, 9])

        self.notes = {}
        self.player_entries = {}
        self.puzzle_entries = {}
        for i in range(9):
            for j in range(9):
                if (n := self.board_array[i, j]) != 0:
                    self.puzzle_entries[(i, j)] = n
        dirty = True

    def cache_until_dirty(func):
        global dirty
        if len(signature(func).parameters):

            def wrapper(*args):
                if dirty:
                    wrapper.cache = {}
                if args not in wrapper.cache:
                    wrapper.cache[args] = func(*args)
                return wrapper.cache[args]

        else:

            def wrapper():
                if dirty:
                    wrapper.cache = func()
                return wrapper.cache

        return wrapper

    @cache_until_dirty
    def __getitem__(self, cell):
        return self.board_array[cell]

    def __setitem__(self, cell, n):
        global dirty
        if cell not in self.puzzle_entries:
            dirty = True
            self.board_array[cell] = n
            if n == 0:
                self.player_entries.pop(cell, None)
            else:
                self.player_entries[cell] = n

    @cache_until_dirty
    def check(self):
        bad_cells = set()
        for group in ALL_GROUPS:
            group_values = set()
            repeated_values = set()
            for cell in group:
                n = self.board_array[cell]
                if n == 0:
                    continue
                elif n not in group_values:
                    group_values.add(n)
                else:
                    repeated_values.add(n)
            for cell in group:
                n = self.board_array[cell]
                if n in repeated_values:
                    bad_cells.add(cell)
        return bad_cells

    def get_note(self, cell):
        return self.notes.get(cell, set())

    def get_all_notes(self):
        return self.notes

    def make_note(self, cell, n):
        if not self[cell]:
            self.notes[cell] = self.notes.get(cell, set()) ^ {n}

    def get_all_same(self, n):
        l = []
        if n:
            cells = np.argwhere(self.board_array == n)
            [l.append(tuple(c)) for c in cells]
        return l
