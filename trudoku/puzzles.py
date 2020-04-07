from random import choice


def get_puzzle(difficulty):
    with open("puzzles/" + difficulty + ".sdm") as f:
        # could not read whole file I guess
        lines = f.read().splitlines()
        return choice(lines).strip()
