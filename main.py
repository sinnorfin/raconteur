# RACONTEUR V0.035
import pyglet
import math
import random

import store
import player
import controls

from pyglet.window import key
from pyglet.window import mouse
from pyglet import clock
from pyglet.gl import *
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, 
                GL_NEAREST)
class Game(object):
    def __init__(self):
        g_player = player.Player(coor=[1,1],img='pchar',id=1)
        controls.cplayer = store.store['gp'][controls.inturn]
        controls.sp_topath = controls.cplayer   
        controls.goal = controls.cplayer
        control = controls.Play()
        store.clevel.push_handlers(controls.Play)
def inarea(m_coor,area):
    if (m_coor[0] >= area.coor[0][0] and
        m_coor[0] <= area.coor[0][1] and
        m_coor[1] >= area.coor[1][0] and
        m_coor[1] <= area.coor[1][1]):
        return True
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
def prange(loc):
    range = control.cplayer.distance(loc)
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
    def on_mouse_motion(x,y,dx,dy):
        if (x+self.anctile > Cursor.mposx + self.tilesize or
            x+self.anctile < Cursor.mposx or 
            y+self.anctile > Cursor.mposy + self.tilesize or 
            y+self.anctile < Cursor.mposy ):
            if ontiles([x,y],Path.ptagged):
                Cursor.xcoor = math.floor(x/self.tilesize)
                Cursor.ycoor = math.floor(y/self.tilesize)
                Cursor.cursor = pyglet.sprite.Sprite( 
                             x =store.clevel.ct(Cursor.xcoor),
                             y =store.clevel.ct(Cursor.ycoor),
                             img = self.image['cursor'])          
                Cursor.mposx = Cursor.cursor.x 
                Cursor.mposy = Cursor.cursor.y 
                Cursor.coor = [Cursor.xcoor, Cursor.ycoor]
                Cursor.onarea = 'm'
                Path.clean_Path(tags=False)
                Path.goal = store.findtile(Cursor.coor)
                control.cplayer.pathing()
        return True
    @staticmethod
    def on_mouse_press(x,y,button,modifiers): 
        if button == mouse.LEFT: 
            if ontiles([x,y],Path.ptagged):
                Path.clean_Path()
                Path.goal = store.findtile(Cursor.coor)
                control.cplayer.pathing()
                control.cplayer.pmove(Path.cpath.nodes,
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
            control.cplayer.pmove(Path.cpath.nodes,Path.step)
        if animated.x < goal.x:
            control.cplayer.look = 'pchar'
            animated._set_image(self.image[control.cplayer.look])
            animated.x += 10
        if animated.y < goal.y:
            control.cplayer.look = 'pcharB'
            animated._set_image(self.image[control.cplayer.look])
            animated.y += 10
        if animated.x > goal.x:
            control.cplayer.look = 'pcharR'
            animated._set_image(self.image[control.cplayer.look])
            animated.x -= 10
        if animated.y > goal.y:
            control.cplayer.look = 'pcharF'
            animated._set_image(self.image[control.cplayer.look])
            animated.y -= 10   
def update(dt):
    if Path.anim == True:
        Anim.movetoward(Path.node.connect(),
                        control.cplayer.connect())
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, (1.0/30.0))
    game = Game()
    pyglet.app.run()
