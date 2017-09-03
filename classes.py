#!/usr/bin/python
# -*- coding: utf-8 -*-
from maze import *


class Player(object):
    """docstring for Player."""

    def __init__(self, mode=1):
        super(Player, self).__init__()

        self.pos = (1, 3)  # (Y,X)
        self.prev = (1, 4)
        self.keys = 0
        self.icon = "⇉"

    def give_key(self):
        self.keys += 1
        pass

    def has_key(self):
        if self.keys <= 0:
            return False
        else:
            self.keys -= 1
            return True

    def move(self, topmsg, lmaze, x=0, y=0):

        newpos = (self.pos[0] + y, self.pos[1] + x)
        wall = "█"
        gates = ["‖", "="]
        key = "⥉"
        msg = topmsg

        allowed = False

        if lmaze[newpos[0]][newpos[1]] == wall:
            pass
        elif lmaze[newpos[0]][newpos[1]] == key:
            self.give_key()
            allowed = True
            msg = keyline
        elif lmaze[newpos[0]][newpos[1]] in gates:
            if self.has_key():
                msg = gateline2
                allowed = True
            else:
                msg = gateline
        else:
            allowed = True

        if allowed:
            self.prev = self.pos
            self.pos = newpos

        return msg

    def set_icon(self, i):
        self.icon = i
        pass

    def get_icon(self):
        return self.icon

    def get_pos(self, v, p=0):
        if p == 0:
            a = self.pos
        else:
            a = self.prev

        if v == 0:
            return a[0]
        else:
            return a[1]
