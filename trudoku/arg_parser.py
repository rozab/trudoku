import argparse

parser = argparse.ArgumentParser(
    prog="trudoku", description="Press ? inside the app for help with keybinds."
)

parser.add_argument(
    "-c",
    "--compact",
    help="force compact mode",
    default=False,
    action="store_true",
    dest="force_compact",
)
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
