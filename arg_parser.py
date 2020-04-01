import argparse

parser = argparse.ArgumentParser(prog="Trudoku", description="ncurses sudoku game")

parser.add_argument(
    "-p",
    "--puzzle",
    nargs="?",
    help="a string of digits representing a puzzle",
    dest="puzzle",
)
parser.add_argument(
    "-f",
    "--font",
    nargs="?",
    help="which ascii art font to use for large numbers",
    choices=["straight", "smshadow"],
    default="straight",
    dest="font",
)
