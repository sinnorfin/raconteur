from pyglet.window import key


import store
import math
import level
##import label
#Probably no need for these
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


def turn():
    store.core.inturn += 1
    playnum = len(store.core.store['gp'])
    if store.core.inturn == playnum:
        store.core.inturn = 0
    store.core.cplayer = store.core.store['gp'][store.core.inturn]
## MOVE out of here
    #Label.create(store.cplayer.name,
    #              Label.playername_label)
