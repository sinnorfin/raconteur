from pyglet.window import key
import store

def turn():
    store.inturn += 1
    playnum = len(store.store['gp'])
    if store.inturn == playnum:
        store.inturn = 0
    store.cplayer = store.store['gp'][store.inturn]
    store.playername_label.text = store.cplayer.name
