#!/usr/bin/python
# -*- coding: utf-8 -*-

from strings import *
import random

# Player Class


class Player(object):
    """docstring for Player."""

    def __init__(self):
        super(Player, self).__init__()

        self.pos = (1, 3)  # (Y,X)
        self.prev = (1, 4)
        self.keys = 0
        self.icon = "⇉"
        self.coins = 0
        self.t_coins = 0
        self.lives = 1
        self.recent_coin = False

        self.lives_received = set()

    # Called when the player dies
    def reset(self, d=0):
        # Reset pos
        self.pos = (1, 3)  # (Y,X)
        self.prev = (1, 4)
        self.icon = "⇉"

        # Remove any coins gained in the current level, to ensure no duplicates
        if d == 1:
            self.t_coins -= self.coins

        # Reset these so they can't dupe items
        self.keys = 0
        self.coins = 0
        self.recent_coin = False
        pass

    # To skip ahead a level
    def jump_level(self):
        self.coins = 0
        self.reset()
        pass

    def full_reset(self):
        self.reset()
        self.lives = 1
        self.t_coins = 0
        self.lives_received = set()

    # Pretty self-explanatory
    def give_key(self):
        self.keys += 1
        pass

    # Ditto
    def give_coin(self):
        self.coins += 1
        self.t_coins += 1
        self.recent_coin = True
        pass

    # Checks if player got a coin last move.
    def got_coin(self):
        return self.recent_coin

    # Double whammy function which takes a key from them if they have one,
    # as this is called as a conditional in move() to let them pass
    def has_key(self):
        if self.keys <= 0:
            return False
        else:
            self.keys -= 1
            return True

    # Moves the player
    def move(self, topmsg, lmaze, x=0, y=0):

        # Calculate player's desired position
        newpos = (self.pos[0] + y, self.pos[1] + x)
        newpos_item = lmaze[newpos[0]][newpos[1]]

        # Set some variables
        wall = "█"
        coin = "⊙"
        gates = ["‖", "=", "}"]
        key = ["⥉", "+"]
        msg = topmsg

        allowed = False
        self.recent_coin = False

        if newpos_item == wall:
            pass
        elif newpos_item == coin:
            self.give_coin()
            allowed = True
            msg = msg_got_coin
        elif newpos_item in key:
            self.give_key()
            allowed = True
            msg = msg_got_key
        elif newpos_item in gates:
            if self.has_key():
                msg = msg_gate_opened
                allowed = True
            else:
                msg = msg_gate_locked
        else:
            allowed = True

        if allowed:
            self.prev = self.pos
            self.pos = newpos

        for i in range(5, 100, 5):
            if self.t_coins >= i and i not in self.lives_received:
                self.lives_received.add(i)
                self.lives += 1
                msg = msg_got_life

        # if self.t_coins % 5 == 0 and self.got_coin():
        #     self.lives += 1
        #     msg = msg_got_life

        return msg

    # Self-explanatory
    def set_icon(self, i):
        self.icon = i
        pass

    # Again
    def get_icon(self):
        return self.icon

    # Returns one element of the player's position, from current or previous
    def get_pos(self, v, p=0):
        if p == 0:
            a = self.pos
        else:
            a = self.prev

        if v == 0:
            return a[0]
        else:
            return a[1]

    # Returns a tuple of the player's pos
    def get_pos_tuple(self, p=0):
        if p == 0:
            return self.pos
        else:
            return self.prev


# Enemy Class
class Enemy(object):
    """docstring for Enemy."""

    def __init__(self, y, x):
        super(Enemy, self).__init__()

        self.initargs = (y, x)
        self.pos = (y, x)  # (Y,X)
        self.prev = (y, x + 1)
        self.icon = "✧"
        self.dir = (0, 1)

    # Resets the enemy to its original location
    def reset(self):
        self.pos = self.initargs  # (Y,X)
        self.prev = (10, 32)

    # Moves the enemy in its current direction unless it will hit a wall, then turn
    def move(self, lmaze):

        special_items = ["█"]  # , "‖", "="]  # , "⥉", "⊙"]
        dir_list = [(1, 0), (0, -1), (-1, 0), (0, 1)]

        # Random movement

        random.shuffle(dir_list)

        if lmaze[self.pos[0] + self.dir[0]][self.pos[1] + self.dir[1]] in special_items:
            for i in dir_list:
                if lmaze[self.pos[0] + i[0]][self.pos[1] + i[1]] not in special_items:
                    self.prev = self.pos
                    self.pos = (self.pos[0] + i[0], self.pos[1] + i[1])
                    self.dir = i
                    break

        else:
            self.prev = self.pos
            self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        return

    # Returns the enemy icon
    def get_icon(self):
        return self.icon

    # Returns one element of the enemy's position, from current or previous
    def get_pos(self, v, p=0):
        if p == 0:
            a = self.pos
        else:
            a = self.prev

        if v == 0:
            return a[0]
        else:
            return a[1]

    # Returns a tuple of the enemy's pos
    def get_pos_tuple(self, p=0):
        if p == 0:
            return self.pos
        else:
            return self.prev
