from pyglet.window import key
from pyglet.sprite import Sprite

import store
import math
import level
##import label
class Vars(object):
    def __init__(self):
        waypoint = False
        sp_topath = ''
        goal = ''
        goalwp = ''
        obstacles = []
        distances = []
        xlist = []
        ylist = []
        handleraltered = False

def turn():
    store.inturn += 1
    playnum = len(store.core.store['gp'])
    if store.inturn == playnum:
        store.inturn = 0
    store.cplayer = store.core.store['gp'][store.core.inturn]
## MOVE out of here
    #Label.create(store.cplayer.name,
    #              Label.playername_label)
