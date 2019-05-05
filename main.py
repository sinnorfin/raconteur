# RACONTEUR V0.035
import pyglet
import math
import random

import store
import player
import gui
import controls
import level

from pyglet.window import key
from pyglet.window import mouse
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
        store.clevel.levelgen()
        store.cursor = gui.Cursor()
        g_player = player.Player(coor=[1,1],img='pchar',id=1)
        store.core.cplayer = store.core.store['gp'][store.core.inturn]
        controls.sp_topath = store.core.cplayer
        controls.goal = store.core.cplayer

        #NO class functions?
def ontiles(m_coor,tiles):
    for tile in tiles:
        if (m_coor[0] >= store.clevel.ct(tile.coor[0])-self.anctile and
            m_coor[0] <= store.clevel.ct(tile.coor[0])+self.anctile and
            m_coor[1] >= store.clevel.ct(tile.coor[1])-self.anctile and
            m_coor[1] <= store.clevel.ct(tile.coor[1])+self.anctile):
            return True
def delol(overloc,ol):
    ol.connect(True,delete=True).delete()
    overloc.overlays.remove(ol)
    if len(overloc.overlays) == 0:
        overloc.occup = False
        #NO return?
        #Deletes overlays from tile and makes it unoccopied
def prange(loc):
    range = store.cplayer.distance(loc)
    # range[0] = distance in absolute units on x axis [1] = y axis
    return range
def getfunc(funct):
    for func in Gui.rcm[1].clickloc.functions:
        if func.func == funct:
            return func
def getol(funct):
    for ol in Gui.rcm[1].clickloc.overlays:
        if ol.func == funct:
            return ol
def lock():
    getfunc('door').locked = True
def unlock():
    getfunc('door').locked = False
def pickup():
    delol(Gui.rcm[1].clickloc,getol('item_p'))
class Path(object):
    cost = 0
    tagged = []
    ptagged = []
    tags = []
    wp = []
    goal = None
    pl = []
    cpath = None
    anim = False
    step = 0
    @staticmethod
    def clean_Path(tags=True):
        Path.cost = 0
        Path.tagged[:] = []
        Path.pl[:] = []
        if Path.wp:
            for wp in Path.wp:
                wp.delete
        del Path.wp[:]
        if tags == True:
            for tag in Path.tags:
                tag.delete()
            del Path.tags[:]
    @staticmethod
    def on_key_press(symbol,modifiers):
        if symbol == key.ESCAPE:
            self.game_window.pop_handlers()
            control.handleraltered = False
            Path.clean_Path()
            del Path.ptagged[:]
            return True
    @staticmethod
    def on_mouse_press(x,y,button,modifiers):
        if button == mouse.LEFT:
            if ontiles([x,y],Path.ptagged):
                Path.clean_Path()
                Path.goal = store.findtile(Cursor.coor)
                store.cplayer.pathing()
                store.cplayer.pmove(Path.cpath.nodes,
                                            Path.step)
                del Path.ptagged[:]
                Path.clean_Path()
                self.game_window.pop_handlers()
                control.handleraltered = False
            return True
    def __init__(self,cost,nodes):
        self.cost = cost
        self.nodes = nodes
class Anim(object):
    @staticmethod
    def movetoward(goal,animated):
        if (animated.x == goal.x and
            animated.y == goal.y):
            Path.anim = False
            Path.step += 1
            store.cplayer.pmove(Path.cpath.nodes,Path.step)
        if animated.x < goal.x:
            store.cplayer.look = 'pchar'
            animated.image=self.image[store.cplayer.look]
            animated.x += 10
        if animated.y < goal.y:
            store.cplayer.look = 'pcharB'
            animated.image=self.image[store.cplayer.look]
            animated.y += 10
        if animated.x > goal.x:
            store.cplayer.look = 'pcharR'
            animated.image=self.image[store.cplayer.look]
            animated.x -= 10
        if animated.y > goal.y:
            store.cplayer.look = 'pcharF'
            animated.image=self.image[store.cplayer.look]
            animated.y -= 10
def update(dt):
    if Path.anim == True:
        Anim.movetoward(Path.node.connect(),
                        store.cplayer.connect())
game = Game()
@store.clevel.event
def on_draw():
    #separate dynamic from static -optimization
    store.clevel.clear()
    store.map_bt.draw()
    store.debug_bt.draw()
    store.item_bt.draw()
    store.player_bt.draw()
    #Level.buildmenu.label.draw()
    store.cursor.sp.draw()
    store.menu_bt.draw()
@store.clevel.event
def on_key_press(self,symbol,modifiers):
    if symbol == key.UP:
        store.cplayer.moveup()
    elif symbol == key.DOWN:
        store.cplayer.movedown()
    elif symbol == key.LEFT:
        store.cplayer.moveleft()
    elif symbol == key.RIGHT:
        store.cplayer.moveright()
    elif symbol == key.SPACE:
        if not store.cplayer.cols():
            if store.cplayer.img == 'pchar':
                store.cplayer.connect().image= store.image['pchar_1b']
                store.cplayer.img = 'pchar_1b'
            else:
                store.cplayer.connect().image= store.image['pchar']
                store.cplayer.img = 'pchar'
            turn()
    elif symbol == key.B:
        if not store.cplayer.cols():
            if gui.SelBuild.c[1] == 1:
                gui.SelBuild.overlay(gui.SelBuild.buildlist[
                                 gui.SelBuild.c[0]][0],
                        store.cplayer.coor,
                        findtile(store.cplayer))
                turn()
            else:
                gui.SelBuild.build(gui.SelBuild.buildlist[
                                    gui.SelBuild.c[0]][0],
                        store.cplayer.coor,
                        findtile(store.cplayer))
                turn()
    elif symbol == key.P:
        store.cplayer.addplayer()
    elif symbol == key.DELETE:
        dellevel(delol=True)
        game.newlevel()
    elif symbol == key.R:
        dellevel(delol=True)
        game.newlevel()
        Spawn.g_object(8,type = 'wall')
    elif symbol == key.S:
        store.clevel.savelevel()
    elif symbol == key.L:
        store.clevel.loadlevel()
        turn()
    elif symbol == key.Q:
        gui.SelBuild.next(self)
    elif symbol == key.O:
        print (len(store.cplayer.player_bordering()))
    elif symbol == key.T:
        pushhandlers(Typein)
        Typein.firstt = True
    elif symbol == key.M:
        pushhandlers(Path)
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
def on_mouse_press(self,x,y,button,modifiers):
    clickloc = findtile(store.cursor.coor)
    if button == mouse.LEFT:
        if (Gui.rcm[0] and gui.inarea(store.cursor.coor,
            store.clevel.levelarea)):
            Gui.rcm[1].click([x,y])
        elif (not Gui.rcm[0] and gui.inarea(store.cursor.coor,
            store.clevel.levelarea)):
            for func in clickloc.functions:
                if (func.func == 'door' and
                    level.adj(store.cplayer,
                                  clickloc)):
                        func.use(clickloc)
        #elif store.store['gt']:
            #for g_tile in store.store['gt']:
                #if store.cursor.coor == g_tile.coor:
                    #if not level.standon(
                        #store.cplayer, g_tile):
                            #pathto(
                                #store.cplayer,g_tile)
    elif button == mouse.RIGHT:
        if gui.inarea([x,y],store.clevel.levelarea):
            print ('MENNU')
            if Gui.rcm[0]:
               Gui.killrcm()
            rcm = Gui([x,y],'rcm',clickloc)
            Gui.rcm.append(rcm)
        else: print ('NOMENU')
    elif button == mouse.MIDDLE:
        print (len(clickloc.functions))
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, (1.0/30.0))
    pyglet.app.run()
