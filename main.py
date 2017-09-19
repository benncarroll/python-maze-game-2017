#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################
##       Dependencies.      ##
##############################

import sys
import subprocess
import curses
import random
from time import sleep

##############################
##      Custom Modules.     ##
##############################

from classes import *
from mazes import *
from strings import *

##############################
##     Global Variables.    ##
##############################

# Change this to enable level skipping, more info, etc.
debug = False

lmaze = list()
p = Player()
e = list()
maze_coins = 0
top_msg = ""
special_items = ["⥉", "‖", "⊙", "=", "+", "}"]
cmaze = 0
recovering = 3
reco_count = 0

##############################
##      Size checking.      ##
##############################


def startup():
    # Get dimensions of Terminal
    tr, tc = subprocess.check_output(['stty', 'size']).decode().split()
    ts = True
    while ts:
        # Define inside loop so that it is run once.
        ts = True if int(tr) < 24 or int(tc) < 77 else False

        # Construct message
        msg = str_ts + str_opt if ts else str_opt

        print(str_main.format(msg))

        decision = input("\n").lower()
        decision = decision if decision else " "

        if decision[0] == "y":
            ts_scpt = """tell application "Terminal"
                set bounds of front window to {0, 0, 1920, 1080}
            end tell

            tell application "System Events"
                keystroke "0" using {command down}
                repeat 14 times
                    key code 69 using {command down}
                end repeat
            end tell"""

            # Run applescript to resize terminal to desired dimensions
            proc = subprocess.Popen(['osascript', '-'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
            stdout_output = proc.communicate(ts_scpt)[0]

        tr, tc = subprocess.check_output(['stty', 'size']).decode().split()
        ts = True if int(tr) < 24 or int(tc) < 77 else False

    print("")

##############################
##       Title Screen.      ##
##############################


def title_screen(screen, d=0):
    # Modes:
    # 0 is for default opening
    # 1 is for death
    # 2 is for completed level
    # 3 is for finishing the game
    # 4 is for when you get a coin

    global maze_coins
    global cmaze
    global recovering

    a = 0

    # Set timeout to infinite so title screen is not skipped.
    screen.timeout(-1)

    # Added to clear previous game if player has died.
    screen.clear()

    # Change messages dependent on death
    if d == 0:
        sleep(1)
        screen.clear()
        screen.refresh()
        dims = screen.getmaxyx()
        # Print out big ASCII art intro
        for i, text in enumerate(intro.splitlines()):
            screen.addstr(i, dims[1] // 2 - len(text) // 2, text, curses.color_pair(3) | curses.A_BOLD)

    elif d == 1:

        # Take a life, change player colour to red
        p.lives -= 1
        recovering = 2

        l1 = "You died"

        # If they have lives, let them continue, else start the whole game again.
        if p.lives >= 1:
            l3 = "You have {} life(s) left.".format(p.lives)
            l2 = "Press any key to continue this level."
            a = 1
        else:
            l1 += " and have ran out of lives."
            l3 = "You got a total of {} points.".format(p.t_coins)
            l2 = "Press any key to start again."
            recovering = 3
            p.full_reset()
            cmaze = 1 if cmaze >= 2 else 0

    elif d == 2:
        p.reset()
        l1 = "Level Completed"
        l2 = "Press any key to continue."
        l3 = "You received 5 bonus points."

    elif d == 3:
        p.reset()
        cmaze = 1
        l1 = "Congratulations! You finished the game!"
        l3 = "Your final score was {}.".format(p.t_coins)
        l2 = "If you would like to play again, press R."

    elif d == 4:
        screen.timeout(-1)
        p.recent_coin = False
        l4 = "You got a coin!"
        l1 = "If you're not coping, you can wimp out! (no pressure)"
        l3 = "It'll cost you points-wise though."
        l2 = "Press Y to skip, or any other key to continue this level."

    # Get dims of terminal with curses
    dims = screen.getmaxyx()

    # Print title screen lines
    if d != 0 and d != 5:
        l4 = " " if 'l4' not in locals() else l4
        screen.addstr(dims[0] // 2 - 4, dims[1] // 2 - (len(l4) // 2), l4, curses.color_pair(3) | curses.A_BOLD)
        screen.addstr(dims[0] // 2 - 2, dims[1] // 2 - (len(l1) // 2), l1, curses.color_pair(3) | curses.A_BOLD)
        screen.addstr(dims[0] // 2 + 0, dims[1] // 2 - (len(l3) // 2), l3, curses.color_pair(3) | curses.A_BOLD)
        screen.addstr(dims[0] // 2 + 2, dims[1] // 2 - (len(l2) // 2), l2, curses.color_pair(4) | curses.A_STANDOUT)

    # Update lines
    screen.refresh()

    # Sleep so titles aren't accidentally skipped.
    z = 1 if d != 4 else 2
    sleep(z)

    # Wait for user's input to pass title screen
    if d != 5:
        screen.timeout(-1)
    elif d == 5:
        p.jump_level()
        screen.timeout(1)
    key = screen.getch()
    if d != 4 and a != 1:
        if d == 3:
            die = True
            if key == 82 or key == 114:
                die = False
            if die:
                sys.exit("-" * 25 + " Thanks for playing! Score: {} ".format(p.t_coins) + "-" * 25)

        if key == 113 or key == 81:
            sys.exit("-" * 25 + " Thanks for playing! Score: {} ".format(p.t_coins) + "-" * 25)

        # Check if they have completed all mazes
        if cmaze >= len(mazes):
            title_screen(screen, 3)

        # Read in maze from file.
        del lmaze[:]
        pmaze = [y for y in (x.strip() for x in mazes[cmaze].splitlines()) if y]
        cmaze += 1
        for i in pmaze:
            lmaze.append(list(i))

        # Scan in enemies & coins
        del e[:]
        maze_coins = 0
        for r, row in enumerate(lmaze):
            for c, column in enumerate(row):
                if column == "✧":
                    e.append(Enemy(r, c))
                    lmaze[r][c] = " "
                if column == "⊙":
                    maze_coins += 1

        # Remove the challenege found in the bottom.
        maze_coins -= 1

    elif d == 4:
        if key == 81 or key == 121:
            p.recent_coin = False
            title_screen(screen, 5)


##############################
##     Print Play Area.     ##
##############################


def print_map(screen):

    # This function uses the curses module to display the map and other
    # items on the screen. It centers all content, enemies and the map using
    # mathemagics.

    global recovering

    screen.clear()

    dims = screen.getmaxyx()

    # Print out maze line by line
    for i, content in enumerate(lmaze):
        string = ''.join(content)  # + "\n"
        screen.addstr(dims[0] // 2 - 12 + i, dims[1] // 2 - (len(string) // 2), string, curses.color_pair(6))

    # Show spaces
    for enemy in e:
        screen.addstr(dims[0] // 2 - 12 + enemy.get_pos(0, 1), dims[1] // 2 - len(lmaze[0]) //
                      2 + enemy.get_pos(1, 1), ' ',              curses.color_pair(0))
    screen.addstr(dims[0] // 2 - 12 + p.get_pos(0, 1), dims[1] // 2 - len(lmaze[0]) // 2 + p.get_pos(1, 1), ' ', curses.color_pair(0))

    # Replace player's last position on the board with a space
    lmaze[p.get_pos(0, 1)][p.get_pos(1, 1)] = " "

    # Colorise special items (gates, keys, coins)
    for r, row in enumerate(lmaze):
        for c, column in enumerate(row):
            if column in special_items:
                screen.addstr(dims[0] // 2 - 12 + r, dims[1] // 2 - len(lmaze[0]) // 2 + c, column, curses.color_pair(4))

    # Display player's position
    screen.addstr(dims[0] // 2 - 12 + p.get_pos(0), dims[1] // 2 - len(lmaze[0]) //
                  2 + p.get_pos(1), p.get_icon(), curses.color_pair(recovering) | curses.A_BOLD)

    # Display enemies
    for enemy in e:
        screen.addstr(dims[0] // 2 - 12 + enemy.get_pos(0),  dims[1] // 2 - len(lmaze[0]) //
                      2 + enemy.get_pos(1),    enemy.get_icon(), curses.color_pair(2))

    # Show top_msg
    screen.addstr(0, dims[1] // 2 - (len(top_msg) // 2), top_msg, curses.color_pair(1))

    # Show score, lives, coins, etc.
    screen.addstr(dims[0] // 2 + 8, dims[1] // 2 - (len(lmaze[0]) // 2) + 1, "Score: {} Lives: {}".format(p.t_coins, p.lives), curses.color_pair(1))
    screen.addstr(dims[0] // 2 + 8, dims[1] // 2 + (len(lmaze[0]) // 2) - 19, "Level: {} Keys: {}".format(cmaze, p.keys), curses.color_pair(1))

    # Debug Info
    if debug:
        screen.addstr(0, 0, "Debug Info:", curses.color_pair(1))
        screen.addstr(1, 0, "Coins: {} Total: {} RC: {} Lives: {} Set: {}".format(
            p.coins, p.t_coins, p.got_coin(), p.lives, p.lives_received), curses.color_pair(1))

    screen.refresh()
    pass


##############################
##        Main Loop.        ##
##############################


def main(screen):

    # Main while loop which loops infintely, updating enemies, player and a
    # bunch of other stuff.

    global top_msg
    global maze_coins
    global recovering
    global reco_count

    # More curses jazz
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.curs_set(0)

    # Intro
    title_screen(screen)

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

        # Recovering counter
        if recovering == 2:
            reco_count += 1
            if reco_count >= 10:
                recovering = 3
                reco_count = 0

        # Hide notifications (top_msg) after 10 moves.
        if msg_count >= 10 and top_msg == old_msg:
            msg_count = 0
            top_msg = ""
        elif top_msg == old_msg:
            msg_count += 1
        elif top_msg != old_msg:
            msg_count = 0

        # Check death
        if recovering == 3:
            for i in e:
                if i.get_pos_tuple() == p.get_pos_tuple():
                    title_screen(screen, 1)
                    break

        print_map(screen)

        screen.timeout(100)
        key = screen.getch()

        # Check for quit
        if key == 113 or key == 81:
            sys.exit("-" * 25 + " Thanks for playing! Score: {} ".format(p.t_coins) + "-" * 25)

        # Check for tutorial
        if key == 116 or key == 114:
            cmaze = 0
            title_screen(screen, 0)
            print_map(screen)

        if debug:
            if key == 103:
                p.give_coin()

            # Skip ahead for testing DEBUG
            if key == 83 or key == 115:
                title_screen(screen, 2)

        # Check if they got a coin that round
        if p.got_coin() and p.coins < maze_coins:
            title_screen(screen, 4)

        # Check if they have gotten all coins
        if p.coins >= maze_coins:
            for i in range(5):
                p.give_coin()
            title_screen(screen, 2)


##############################
##    Program Execution.    ##
##############################

startup()
curses.wrapper(main)
