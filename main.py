#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import curses
from time import sleep

# My files
from classes import *
from maze import *

# Globals
lmaze = list()
p = Player()
# e1 = Player(0)
top_msg = ""
special_items= ["⥉", "‖", "⊙"]


def start_game(screen):
    dims = screen.getmaxyx()
    l1 = "Welcome to Carroll's CYOA Game."
    l2 = "Press any key to start."
    l3 = "Press Q at any time to quit."
    screen.addstr(dims[0] // 2 - 2, dims[1] // 2 - (len(l1) // 2), l1, curses.color_pair(3) | curses.A_BOLD)
    screen.addstr(dims[0] // 2 + 0, dims[1] // 2 - (len(l3) // 2), l3, curses.color_pair(3) | curses.A_BOLD)
    screen.addstr(dims[0] // 2 + 2, dims[1] // 2 - (len(l2) // 2), l2, curses.color_pair(4) | curses.A_STANDOUT)

    screen.refresh()

    e = screen.getch()
    if e == 113 or e == 81:
        sys.exit("Game quit.")


def print_map(screen):
    dims = screen.getmaxyx()

    for i, content in enumerate(lmaze):
        string = ''.join(content) # + "\n"
        # if i > 20:
        #     screen.addstr(i, dims[1] // 2 - (len(string) // 2), string)
        # else:
        screen.addstr(i, 0, string, curses.color_pair(6))

    # Colorise items
    for r, row in enumerate(lmaze):
        for c, column in enumerate(row):
            if column in special_items:
                screen.addstr(r, c, column, curses.color_pair(4))


    # Display player's position
    screen.addstr(p.get_pos(0), p.get_pos(1), p.get_icon(), curses.color_pair(2))
    screen.addstr(p.get_pos(0, 1), p.get_pos(1, 1), ' ', curses.color_pair(0))
    lmaze[p.get_pos(0, 1)][p.get_pos(1, 1)] = " "


    # Show top_msg
    screen.addstr(0, dims[1] // 2 - (len(top_msg) // 2),
                  top_msg, curses.color_pair(1))

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

    # Read in maze from file once.
    pmaze = [y for y in (x.strip() for x in fmaze.splitlines()) if y]
    for i in pmaze:
        lmaze.append(list(i))

    # Print map
    print_map(screen)

    # Begin Looping
    key = screen.getch()
    msg_count = 0
    while key:

        old_msg = top_msg

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

        if msg_count >= 10 and top_msg == old_msg:
            msg_count = 0
            top_msg = ""
        elif top_msg == old_msg:
            msg_count += 1
        elif top_msg != old_msg:
            msg_count = 0

        print_map(screen)
        # if key == 112:
        # screen.addstr(20,0, "Keys: {} top_msg: {}".format(p.keys, top_msg[:50]))

        key = screen.getch()
        if key == 113 or key == 81:
            sys.exit("Game quit.")


curses.wrapper(main)
