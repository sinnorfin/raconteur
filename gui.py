import random
import pyglet.text
import store
import level
from sp import Sp_Tile

def inarea(m_coor,area):
    if (m_coor[0] >= area.coor[0][0] and
        m_coor[0] <= area.coor[0][1] and
        m_coor[1] >= area.coor[1][0] and
        m_coor[1] <= area.coor[1][1]):
        return True

class Button(object):
    def __init__(self,img,function=None):
        self.img = img
        self.o_coor = [0,0]
        self.function = function
    def drawbut(self,o_coor):
        self.o_coor = o_coor
        button = pyglet.sprite.Sprite(x=o_coor[0],y=o_coor[1],
                                      img=self.image[self.img],
                                      bt = store.menu_batch)
        sp_gui.append(button)
    def press(self):
        self.function()
        print ('you pressed %s' % self.img)
class Gui(object):
    rcmhead = Button('c_menu')
    rcm = [False]
    def __init__(self,o_coor,gtype,clickloc):
        self.o_coor = o_coor
        self.gtype = gtype
        self.clickloc = clickloc
        self.orig = [0,0]
        self.size = [80,50]
        self.buttons = []
        if gtype == 'rcm' and Cursor.onarea == 'l':
                Gui.rcm[0] = True
                self.rightclickmenu()
    def rightclickmenu(self):
        for f in self.clickloc.functions:
            if (max(prange(self.clickloc)) == 1 and
                prange(self.clickloc)[0] != prange(self.clickloc)[1]):
                if f.func == 'door' and f.locked == True:
                    unl_but = Button('c_unl',unlock)
                    self.buttons.append(unl_but)
                elif f.func == 'door' and f.locked == False:
                    lock_but = Button('c_lock',lock)
                    self.buttons.append(lock_but)
        for f in self.clickloc.overlays: #generator
            if max(prange(self.clickloc)) == 0:
                if hasattr(f,'func') and f.func == 'item_p':
                    pickup_but = Button('c_pickup',pickup)
                    self.buttons.append(pickup_but)
        self.fitmenu(len(self.buttons)+1)
        self.refresh_menu()
    def fitmenu(self,c):
        fitx = False
        fity = False
        if (self.o_coor[0]+self.size[0] >
            level.levelarea.coor[0][1]):
            fitx = True
        if (self.o_coor[1]-self.size[1]*c <
            level.levelarea.coor[1][0]):
            fity = True
        if fitx == True and fity == True:
            self.o_coor[0] = self.o_coor[0]-self.size[0]
            self.o_coor[1] = self.o_coor[1]-self.size[1]*c
        elif fitx == True:
            self.o_coor[0] = self.o_coor[0]-self.size[0]
        elif fity == True:
            self.o_coor[1] = self.o_coor[1]+self.size[1]*c
        self.orig = self.o_coor
    def refresh_menu(self):
        Gui.rcmhead.drawbut([self.orig[0],self.orig[1] - 50])
        for b in self.buttons:
            b.drawbut([self.orig[0],self.orig[1] - 100 -
                      self.buttons.index(b)*self.size[1]])
        #self.size helyett button size
    def click(self,m_coor):
        for b in self.buttons:
            button = level.Gamearea(coor=[[b.o_coor[0],
                              b.o_coor[0]+self.image[b.img].width],
                              [b.o_coor[1],
                              b.o_coor[1]+self.image[b.img].height]])
            if inarea(m_coor,button):
                b.press()
        Gui.killrcm()
    @staticmethod
    def killrcm():
        Gui.rcm.pop()
        Gui.rcm[0] = False
        sp_gui = []
class Cursor(object):
    def __init__(self):
        self.mposx = store.core.ats
        self.mposy = store.core.ats
        self.coor = [self.mposx,self.mposy]
        self.sp = pyglet.sprite.Sprite(x=self.mposx,
                                       y=self.mposy,
                                     img=store.core.image['cursor'])
        self.onarea = 'd'
class MousePointer(object):
    def __init__(self):
        self.x = x
        self.y = y
