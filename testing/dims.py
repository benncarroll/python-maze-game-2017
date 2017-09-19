import curses
import time
screen = curses.initscr()
dims = screen.getmaxyx()
try:
    i=0
    up=1
    while True:
        dims = screen.getmaxyx()
        screen.clear()
        if i < 3:
            up = 1
        if i > dims[1] - 12:
            up = -1
        i+=up
        screen.addstr(dims[0]//2, i, 'Wowee!')
        screen.refresh()
        time.sleep(0.05)
    screen.getch()
finally:
    curses.endwin()
