# RACONTEUR V0.035
import pyglet
import math


import store
import player
import gui
import controls
import level
import element
import label

from pyglet.window import key
from pyglet.window import mouse
from pyglet.sprite import Sprite
from pyglet import clock
from pyglet.gl import *
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_NEAREST)
class Game(object):
    def __init__(self):
        pyglet.resource.path = ['res']
        pyglet.resource.reindex()
        store.map_bt = pyglet.graphics.Batch()
        store.item_bt = pyglet.graphics.Batch()
        store.player_bt = pyglet.graphics.Batch()
        store.menu_bt = pyglet.graphics.Batch()
        store.debug_bt = pyglet.graphics.Batch()
        store.core = store.Store()
        store.clevel = level.Level()
        store.buildmenu = level.SelBuild()
        store.clevel.levelgen()
        store.cursor = gui.Cursor()
        store.handleraltered = False;
        g_player = player.Player(coor=[1,1],img='pchar',id=1)
        store.core.cplayer = store.core.store['gp'][store.core.inturn]
        controls.sp_topath = store.core.cplayer
        store.cid = 2
        controls.goal = store.core.cplayer
        label.create('New')
class Anim(object):
    @staticmethod
    def movetoward(goal,animated):
        if (animated.x == goal.x and
            animated.y == goal.y):
            player.Path.anim = False
            player.Path.step += 1
            store.core.cplayer.pmove(player.Path.cpath.nodes,
                                    player.Path.step)
        if animated.x < goal.x:
            store.core.cplayer.look = 'pchar'
            animated.image=store.core.image[
                                    store.core.cplayer.look]
            animated.x += 10
        if animated.y < goal.y:
            store.core.cplayer.look = 'pcharB'
            animated.image=store.core.image[
                                    store.core.cplayer.look]
            animated.y += 10
        if animated.x > goal.x:
            store.core.cplayer.look = 'pcharR'
            animated.image=store.core.image[
                                    store.core.cplayer.look]
            animated.x -= 10
        if animated.y > goal.y:
            store.core.cplayer.look = 'pcharF'
            animated.image=store.core.image[
                                    store.core.cplayer.look]
            animated.y -= 10
def update(dt):
    if player.Path.anim == True:
        Anim.movetoward(player.Path.node.connect(),
                        store.core.cplayer.sp)
game = Game()

def pushhandlers(Class):
    if store.handleraltered == True:
        store.clevel.pop_handlers()
        store.handleraltered = False
    store.clevel.push_handlers(Class)
    store.handleraltered = True
@store.clevel.event
def on_draw():
    #separate dynamic from static -optimization
    store.clevel.clear()
    store.map_bt.draw()
    store.debug_bt.draw()
    store.item_bt.draw()
    store.player_bt.draw()
    store.buildmenu.label.draw()
    store.cursor.sp.draw()
    store.menu_bt.draw()
@store.clevel.event
def on_key_press(symbol,modifiers):
    if symbol == key.UP:
        store.core.cplayer.moveup()
    elif symbol == key.DOWN:
        store.core.cplayer.movedown()
    elif symbol == key.LEFT:
        store.core.cplayer.moveleft()
    elif symbol == key.RIGHT:
        store.core.cplayer.moveright()
    elif symbol == key.SPACE:
        if not store.core.cplayer.cols():
            if store.core.cplayer.img == 'pchar':
                store.core.cplayer.connect().image= store.core.image['pchar_1b']
                store.core.cplayer.img = 'pchar_1b'
            else:
                store.core.cplayer.connect().image= store.core.image['pchar']
                store.core.cplayer.img = 'pchar'
            controls.turn()
    elif symbol == key.B:
        if not store.core.cplayer.cols():
            if store.buildmenu.c[1] == 1:
                store.buildmenu.overlay(store.core.findtile(
                                    store.core.cplayer.coor),
                                    store.buildmenu.blist[
                                    store.buildmenu.c[0]][0],
                        store.core.cplayer.coor)
                controls.turn()
            else:
                store.buildmenu.build(
                                    store.core.findtile(
                                    store.core.cplayer.coor),
                                    store.buildmenu.blist[
                                    store.buildmenu.c[0]][0],
                                    store.core.cplayer.coor)
                controls.turn()
    elif symbol == key.P:
        store.core.cplayer.addplayer()
    elif symbol == key.DELETE:
        level.dellevel(delol=True)
        store.clevel.levelgen()
    elif symbol == key.R:
        level.dellevel(delol=True)
        store.clevel.levelgen()
        level.Spawn.g_object(8,type = 'wall')
    elif symbol == key.S:
        store.clevel.savelevel()
    elif symbol == key.L:
        store.clevel.loadlevel()
        controls.turn()
    elif symbol == key.Q:
        store.buildmenu.next()
    elif symbol == key.O:
        print (len(store.core.cplayer.player_bordering()))
    elif symbol == key.T:
        pushhandlers(label.Typein)
        label.Typein.firstt = True
    elif symbol == key.M:
        pushhandlers(player.Path)
        store.core.cplayer.moveg()
@store.clevel.event
def on_mouse_motion(x,y,dx,dy):
    if (x+store.core.ats > store.cursor.mposx + store.core.ts or
        x+store.core.ats < store.cursor.mposx or
        y+store.core.ats > store.cursor.mposy + store.core.ts or
        y+store.core.ats < store.cursor.mposy ):
        if gui.inarea([x,y],store.clevel.levelarea):
            store.cursor.xcoor = math.floor(x/store.core.ts)
            store.cursor.ycoor = math.floor(y/store.core.ts)
            store.cursor.sp = Sprite(
                         x =store.core.ct(store.cursor.xcoor),
                         y =store.core.ct(store.cursor.ycoor),
                         img = store.core.image['cursor'])
            store.cursor.mposx = x
            store.cursor.mposy = y
            store.cursor.coor = [store.cursor.xcoor, store.cursor.ycoor]
            store.cursor.onarea = 'l'
        else: store.cursor.onarea = 'o'
@store.clevel.event
def on_mouse_press(x,y,button,modifiers):
    clickloc = store.core.findtile(store.cursor.coor)
    if button == mouse.LEFT:
        if (store.rcm[0] and gui.inarea(store.cursor.coor,
            store.clevel.levelarea)):
            store.rcm[1].click([x,y])
        elif (not store.rcm[0] and gui.inarea(store.cursor.coor,
            store.clevel.levelarea)):
            for func in clickloc.functions:
                if (func.func == 'door' and
                    level.adj(store.core.cplayer,
                                  clickloc)):
                        func.use(clickloc)
        #elif store.core.store['gt']:
            #for g_tile in store.core.store['gt']:
                #if store.cursor.coor == g_tile.coor:
                    #if not level.standon(
                        #store.core.cplayer, g_tile):
                            #pathto(
                                #store.core.cplayer,g_tile)
    elif button == mouse.RIGHT:
        if gui.inarea([x,y],store.clevel.levelarea):
            # menu appears only when right clicked
            # on actual level area of window
            if store.rcm[0]:
               gui.Gui.killrcm()
            rcm = gui.Gui([x,y],'rcm',clickloc)
            store.rcm.append(rcm)
    elif button == mouse.MIDDLE:
        print (len(clickloc.functions))
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, (1.0/30.0))
    pyglet.app.run()
