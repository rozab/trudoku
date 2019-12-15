from blessed import Terminal

t = Terminal()
with t.cbreak():
    while True:
        val = t.inkey()
        print(val, ", ", val.code)