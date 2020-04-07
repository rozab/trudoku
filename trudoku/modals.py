def show_help(t, redraw_bg):
    draw_help(t)
    while (val := t.inkey(esc_delay=0, timeout=0.5)) == "":
        if t.resized:
            redraw_bg()
            draw_help(t)


def draw_help(t):
    # box will be 17x33
    box_text = """\
╔═══════════════════════════════╗
║                               ║
║  Use i,j,k,l or arrow keys    ║
║    for movement.              ║
║                               ║
║  Fill in a cell with 1-9 and  ║
║    clear with x or 0.         ║
║                               ║
║  Switch to notes mode with    ║
║    spacebar and toggle a      ║
║    note with 1-9.             ║
║                               ║
║  Show this dialog with ?.     ║
║                               ║
║  Exit with q.                 ║
║                               ║
╚═══════════════════════════════╝"""

    vgap = (t.height - 17) // 2
    hgap = (t.width - 33) // 2

    for n, line in enumerate(box_text.splitlines()):
        print(t.move(vgap + n, hgap) + t.green(line))


def show_victory(t, redraw_bg):
    draw_victory(t)
    while (val := t.inkey(esc_delay=0, timeout=0.5)) != "q":
        if t.resized:
            redraw_bg()
            draw_victory(t)


def draw_victory(t):
    # box will be 12x36
    box_text = """\
╔══════════════════════════════════╗
║                                  ║
║ __      ____ _| |__   ___ _   _  ║
║ \ \ /\ / / _` | '_ \ / _ \ | | | ║
║  \ V  V / (_| | | | |  __/ |_| | ║
║   \_/\_/ \__,_|_| |_|\___|\__, | ║
║                           |___/  ║
║                                  ║
║                                  ║
║                      u did it    ║
║                                  ║
║  press q to exit                 ║
║                                  ║
╚══════════════════════════════════╝"""

    vgap = (t.height - 12) // 2
    hgap = (t.width - 36) // 2

    for n, line in enumerate(box_text.splitlines()):
        print(t.move(vgap + n, hgap) + t.bold_bright_red(line))
