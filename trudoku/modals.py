def show_help(t, redraw_bg):
    draw_help(t)
    while (val := t.inkey(esc_delay=0, timeout=0.5)) == "":
        if t.resized:
            redraw_bg()
            draw_help(t)


def draw_help(t):
    # box will be 16x33
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
║  Show this dialog with ?      ║
║    or H.                      ║
║                               ║
╚═══════════════════════════════╝"""

    vgap = (t.height - 16) // 2
    hgap = (t.width - 33) // 2

    for n, line in enumerate(box_text.splitlines()):
        print(t.move(vgap + n, hgap) + t.green(line))
