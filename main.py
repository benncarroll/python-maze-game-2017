#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import Dependencies
import sys
import subprocess
import curses
from time import sleep

# My files
from classes import *
from maze import *


##############################
##      Size checking.      ##
##############################

# Get dimensions of Terminal
tr, tc = subprocess.check_output(['stty', 'size']).decode().split()
ts = True
while ts:
    # Define inside loop so that it is run once.
    ts = True if int(tr) < 24 or int(tc) < 80 else False
    if ts:
        msg = """
   Your terminal size is
         too small.

  It needs to be at least
     80 cols x 24 rows.

     Please resize your
        terminal and
        press enter.
"""
    else:
        msg = """
   Would you like to play
      the game in it's
       optimal size?
"""

    print("""
-----------------------------
{}
   To resize automatically,
    type 'auto', followed
         by enter.

-----------------------------
""".format(msg))

    if input("") == 'auto':
        ts_scpt = """tell application "Terminal"
            set bounds of front window to {0, 0, 1920, 1080}
        end tell

        tell application "System Events"
            keystroke "0" using {command down}
            repeat 14 times
                key code 69 using {command down}
            end repeat
        end tell"""

        # Run script to resize terminal to desired dimensions
        proc = subprocess.Popen(['osascript', '-'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
        stdout_output = proc.communicate(ts_scpt)[0]

    tr, tc = subprocess.check_output(['stty', 'size']).decode().split()
    ts = True if int(tr) < 24 or int(tc) < 80 else False

# Clear terminal
print("\n" * 100)


##############################
##     Global Variables.    ##
##############################

lmaze = list()
p = Player()
e = [Enemy(1, 50), Enemy(7, 35), Enemy(3, 72)]
top_msg = ""
special_items = ["⥉", "‖", "⊙"]


##############################
##       Title Screen.      ##
##############################

def start_game(screen, d=0):

    # Get dims of terminal with curses
    dims = screen.getmaxyx()

    # Added to clear previous game if player has died.
    screen.clear()

    # Change messages dependent on death
    if d == 0:
        l1 = "Welcome to Carroll's CYOA Game."
        l2 = "Press any key to start."
        l3 = "Press Q at any time to quit."
    else:

        # Set timeout to infinite so title screen is not skipped.
        screen.timeout(-1)

        # Reset enemies & players
        for enemy in e:
            enemy.reset()
        p.reset()

        l1 = "You died."
        l2 = "Press any key to start a new game."
        l3 = " "

    # Print title screen lines
    screen.addstr(dims[0] // 2 - 2, dims[1] // 2 - (len(l1) // 2), l1, curses.color_pair(3) | curses.A_BOLD)
    screen.addstr(dims[0] // 2 + 0, dims[1] // 2 - (len(l3) // 2), l3, curses.color_pair(3) | curses.A_BOLD)
    screen.addstr(dims[0] // 2 + 2, dims[1] // 2 - (len(l2) // 2), l2, curses.color_pair(4) | curses.A_STANDOUT)

    # Update lines
    screen.refresh()

    z = 2 if d == 1 else 0
    sleep(z)

    # Wait for user's input to pass title screen
    key = screen.getch()
    if key == 113 or key == 81:
        sys.exit("-" * 33 + "  Game quit.  " + "-" * 33)

    # Read in maze from file.
    del lmaze[:]
    pmaze = [y for y in (x.strip() for x in fmaze.splitlines()) if y]
    for i in pmaze:
        lmaze.append(list(i))

##############################
##     Print Play Area.     ##
##############################


def print_map(screen):

    screen.clear()

    dims = screen.getmaxyx()

    for i, content in enumerate(lmaze):
        string = ''.join(content)  # + "\n"
        screen.addstr(dims[0] // 2 - 12 + i, dims[1] // 2 - (len(string) // 2), string, curses.color_pair(6))

    # Show spaces:
    for enemy in e:
        screen.addstr(dims[0] // 2 - 12 + enemy.get_pos(0, 1), dims[1] // 2 - 40 + enemy.get_pos(1, 1), ' ',              curses.color_pair(0))
    screen.addstr(dims[0] // 2 - 12 + p.get_pos(0, 1), dims[1] // 2 - 40 + p.get_pos(1, 1), ' ', curses.color_pair(0))
    lmaze[p.get_pos(0, 1)][p.get_pos(1, 1)] = " "

    # Colorise items
    for r, row in enumerate(lmaze):
        for c, column in enumerate(row):
            if column in special_items:
                screen.addstr(dims[0] // 2 - 12 + r, dims[1] // 2 - 40 + c, column, curses.color_pair(4))

    # Display player's position
    screen.addstr(dims[0] // 2 - 12 + p.get_pos(0), dims[1] // 2 - 40 + p.get_pos(1), p.get_icon(), curses.color_pair(3) | curses.A_BOLD)

    # Display enemies
    for enemy in e:
        screen.addstr(dims[0] // 2 - 12 + enemy.get_pos(0),  dims[1] // 2 - 40 + enemy.get_pos(1),    enemy.get_icon(), curses.color_pair(2))

    # Show top_msg
    screen.addstr(0, dims[1] // 2 - (len(top_msg) // 2), top_msg, curses.color_pair(1))

    screen.refresh()
    pass


def main(screen):
    global top_msg

    # More curses jazz
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.curs_set(0)

    # Intro
    start_game(screen)

    # Print map
    print_map(screen)

    # Begin Looping
    key = screen.getch()
    msg_count = 0
    while key:

        old_msg = top_msg

        # Check player's key, act accordingly
        if key == 259 or key == 119:
            # Up
            p.set_icon("⇈")
            top_msg = p.move(top_msg, lmaze, 0, -1)
        elif key == 258 or key == 115:
            #  Down
            p.set_icon("⇊")
            top_msg = p.move(top_msg, lmaze, 0, 1)
        elif key == 261 or key == 100:
            # Right
            p.set_icon("⇉")
            top_msg = p.move(top_msg, lmaze, 1)
        elif key == 260 or key == 97:
            # Left
            p.set_icon("⇇")
            top_msg = p.move(top_msg, lmaze, -1)

        # Update enemy positions
        for enemy in e:
            enemy.move(lmaze)

        # Hide notifications after 10 moves.
        if msg_count >= 10 and top_msg == old_msg:
            msg_count = 0
            top_msg = ""
        elif top_msg == old_msg:
            msg_count += 1
        elif top_msg != old_msg:
            msg_count = 0

        # Check death
        for i in e:
            if i.get_pos_tuple() == p.get_pos_tuple():
                start_game(screen, 1)

        print_map(screen)

        screen.timeout(100)
        key = screen.getch()

        if key == 113 or key == 81:
            sys.exit("-" * 33 + "  Game quit.  " + "-" * 33 + "\n\n\n")


curses.wrapper(main)
