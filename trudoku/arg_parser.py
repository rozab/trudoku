import argparse

parser = argparse.ArgumentParser(
    prog="trudoku", description="Press ? inside the app for help with keybinds."
)

parser.add_argument(
    "-c",
    "--compact",
    help="force compact view",
    default=False,
    action="store_true",
    dest="force_compact",
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
puzzle_group = parser.add_mutually_exclusive_group(required=True)
puzzle_group.add_argument(
    "-E",
    "--easy",
    help="choose an easy puzzle from the bank",
    action="store_const",
    const="easy",
    dest="difficulty",
)
puzzle_group.add_argument(
    "-M",
    "--medium",
    help="choose a medium puzzle from the bank",
    action="store_const",
    const="medium",
    dest="difficulty",
)
puzzle_group.add_argument(
    "-H",
    "--hard",
    help="choose a hard puzzle from the bank",
    action="store_const",
    const="hard",
    dest="difficulty",
)
puzzle_group.add_argument(
    "-I",
    "--impossible",
    help="choose an impossible puzzle from the bank",
    action="store_const",
    const="impossible",
    dest="difficulty",
)
puzzle_group.add_argument(
    "-p", "--puzzle", help="a string of digits representing a puzzle", dest="puzzle",
)
