from pyglet.window import key

import store
import math
import level

def turn():
    store.core.inturn += 1
    playnum = len(store.core.store['gp'])
    if store.core.inturn == playnum:
        store.core.inturn = 0
    store.core.cplayer = store.core.store['gp'][store.core.inturn]
    store.playername_label.text = store.core.cplayer.name
