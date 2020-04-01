# The SmShadow font was originally by Glenn Chappell, as bundled with figlet
# The Straight font was apparently by Bas Meijer,
# meijer@info.win.tue.nl bas@damek.kth.se
# idk I found it on http://patorjk.com/software/taag


def get_digit(font, n):
    """Returns a list of 3 strings, each of length 7,
    each representing a line in the ascii digit."""
    if font == "smshadow":
        return smshadow[n-1]
    elif font == "straight":
        return straight[n-1]


smshadow = [
    ["  _ |  ",
     "    |  ",
     "   _|  "],
    ["  _  ) ",
     "    /  ",
     "  ___| "],
    ["  __ / ",
     "   _ \\ ",
     "  ___/ "],
    ["  | |  ",
     " __ _| ",
     "   _|  "],
    ["   __| ",
     "  __ \\ ",
     "  ___/ "],
    ["   /   ",
     "   _ \\ ",
     " \\___/ "],
    [" __  / ",
     "    /  ",
     "  _/   "],
    ["   _ ) ",
     "   _ \\ ",
     " \\___/ "],
    ["   _ \\ ",
     " \\_  / ",
     "   _/  "]
]

straight = [
    ["       ",
     "   /|  ",
     "    |  "],
    ["  __   ",
     "   _)  ",
     "  /__  "],
    ["  __   ",
     "   _)  ",
     "  __)  "],
    ["       ",
     "  |__| ",
     "     | "],
    ["   __  ",
     "  |_   ",
     "  __)  "],
    ["   __  ",
     "  /__  ",
     "  \__) "],
    ["  ___  ",
     "    /  ",
     "   /   "],
    ["   __  ",
     "  (__) ",
     "  (__) "],
    ["   __  ",
     "  (__\\ ",
     "   __/ "]
]
