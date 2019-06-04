# RACONTEUR V0.035
import pdb
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
def game():
        store.map_bt = pyglet.graphics.Batch()
        store.item_bt = pyglet.graphics.Batch()
        store.player_bt = pyglet.graphics.Batch()
        store.menu_bt = pyglet.graphics.Batch()
        store.debug_bt = pyglet.graphics.Batch()
        store.clevel = level.Level()
        store.buildmenu = level.SelBuild()
        store.clevel.levelgen()
        store.cursor = gui.Cursor()
        store.handleraltered = False;
        g_player = player.Player(coor=[1,1],img='pchar',id=1)
        store.cplayer = store.store['gp'][store.inturn]
        controls.sp_topath = store.cplayer
        store.cid = 2
        controls.goal = store.cplayer
        label.create(store.cplayer.name)
class Anim(object):
    @staticmethod
    def movetoward(goal,animated):
        if (animated.sp.x == goal.x and
            animated.sp.y == goal.y):
            player.Path.anim = False
            player.Path.step += 1
            store.cplayer.pmove(player.Path.cpath.nodes,
                                    player.Path.step)
            animated.updateols()
            animated.updateitems()
        else:
            if animated.sp.x < goal.x:
                store.cplayer.look = 'pchar'
                animated.sp.image=store.image[store.cplayer.look]
                animated.sp.x += 10
            if animated.sp.y < goal.y:
                store.cplayer.look = 'pcharB'
                animated.sp.image=store.image[store.cplayer.look]
                animated.sp.y += 10
            if animated.sp.x > goal.x:
                store.cplayer.look = 'pcharR'
                animated.sp.image=store.image[store.cplayer.look]
                animated.sp.x -= 10
            if animated.sp.y > goal.y:
                store.cplayer.look = 'pcharF'
                animated.sp.image=store.image[store.cplayer.look]
                animated.sp.y -= 10
            animated.updateols()
def update(dt):
    if player.Path.anim == True:
        Anim.movetoward(player.Path.node.sp,
                        store.cplayer)
game()

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
        store.cplayer.moveup()
        store.cplayer.updateols()
        store.cplayer.updateitems()
    elif symbol == key.DOWN:
        store.cplayer.movedown()
        store.cplayer.updateols()
        store.cplayer.updateitems()
    elif symbol == key.LEFT:
        store.cplayer.moveleft()
        store.cplayer.updateols()
        store.cplayer.updateitems()
    elif symbol == key.RIGHT:
        store.cplayer.moveright()
        store.cplayer.updateols()
        store.cplayer.updateitems()
    elif symbol == key.SPACE:
        if not store.cplayer.cols():
            if store.cplayer.img == 'pchar':
                store.cplayer.sp.image= store.image['pchar_1b']
                store.cplayer.img = 'pchar_1b'
            else:
                store.cplayer.sp.image= store.image['pchar']
                store.cplayer.img = 'pchar'
            controls.turn()
    elif symbol == key.B:
        if not store.cplayer.cols():
            if store.buildmenu.c[1] == 1:
                store.buildmenu.overlay(store.findtile(
                                    store.cplayer.coor),
                                    store.buildmenu.blist[
                                    store.buildmenu.c[0]][0],
                        store.cplayer.coor)
                controls.turn()
            else:
                store.buildmenu.build(
                                    store.findtile(
                                    store.cplayer.coor),
                                    store.buildmenu.blist[
                                    store.buildmenu.c[0]][0],
                                    store.cplayer.coor)
                controls.turn()
    elif symbol == key.P:
        store.cplayer.addplayer()
    elif symbol == key.DELETE:
        level.dellevel(delol=True)
        store.clevel.levelgen()
    elif symbol == key.R:
        level.dellevel(delol=True)
        store.clevel.levelgen()
        level.Spawn.g_object(8,type = 'wall')
    elif symbol == key.S:
        level.savelevel()
    elif symbol == key.L:
        level.loadlevel()
        controls.turn()
    elif symbol == key.Q:
        store.buildmenu.next()
    elif symbol == key.O:
        print (len(store.cplayer.player_bordering()))
    elif symbol == key.T:
        label.Typein.firstt = True
        pushhandlers(label.Typein)
    elif symbol == key.M:
        pushhandlers(player.Path)
        store.cplayer.moveg()
@store.clevel.event
def on_mouse_motion(x,y,dx,dy):
    if (x+store.ats > store.cursor.mposx + store.ts or
        x+store.ats < store.cursor.mposx or
        y+store.ats > store.cursor.mposy + store.ts or
        y+store.ats < store.cursor.mposy ):
        if gui.inarea([x,y],store.clevel.levelarea):
            store.cursor.xcoor = math.floor(x/store.ts)
            store.cursor.ycoor = math.floor(y/store.ts)
            store.cursor.sp = Sprite(
                         x =store.ct(store.cursor.xcoor),
                         y =store.ct(store.cursor.ycoor),
                         img = store.image['cursor'])
            store.cursor.mposx = x
            store.cursor.mposy = y
            store.cursor.coor = [store.cursor.xcoor, store.cursor.ycoor]
            store.cursor.onarea = 'l'
        else: store.cursor.onarea = 'o'
@store.clevel.event
def on_mouse_press(x,y,button,modifiers):
    clickloc = store.findtile(store.cursor.coor)
    if button == mouse.LEFT:
        if (store.rcm[0] and gui.inarea(store.cursor.coor,
            store.clevel.levelarea)):
            store.rcm[1].click([x,y])
        elif (not store.rcm[0] and gui.inarea(store.cursor.coor,
            store.clevel.levelarea)):
            for func in clickloc.functions:
                if (func.func == 'door' and
                    level.adj(store.cplayer,
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
