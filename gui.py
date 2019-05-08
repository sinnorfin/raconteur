import random
import pyglet.text
import store
import level
import element
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
                                      img=store.core.image[self.img],
                                      batch = store.menu_bt)
        store.core.store['spg'].append(button)
    def press(self):
        self.function()
        print ('you pressed %s' % self.img)
class Gui(object):
    rcmhead = Button('c_menu')
    store.rcm = [False]
    def __init__(self,o_coor,gtype,clickloc):
        self.o_coor = o_coor
        self.gtype = gtype
        self.clickloc = clickloc
        self.orig = [0,0]
        self.size = [80,50]
        self.buttons = []
        if gtype == 'rcm' and store.cursor.onarea == 'l':
                store.rcm[0] = True
                self.rightclickmenu()
    def rightclickmenu(self):
        for f in self.clickloc.functions:
            if (max(store.prange(self.clickloc)) == 1 and
                store.prange(self.clickloc)[0] != store.prange(self.clickloc)[1]):
                if f.func == 'door' and f.locked == True:
                    unl_but = Button('c_unl',unlock)
                    self.buttons.append(unl_but)
                elif f.func == 'door' and f.locked == False:
                    lock_but = Button('c_lock',lock)
                    self.buttons.append(lock_but)
        for f in self.clickloc.overlays: #generator
            if max(store.prange(self.clickloc)) == 0:
                if hasattr(f,'func') and f.func == 'item_p':
                    pickup_but = Button('c_pickup',element.pickup)
                    self.buttons.append(pickup_but)
        self.fitmenu(len(self.buttons)+1)
        self.refresh_menu()
    def fitmenu(self,c):
        fitx = False
        fity = False
        if (self.o_coor[0]+self.size[0] >
            store.clevel.levelarea.coor[0][1]):
            fitx = True
        if (self.o_coor[1]-self.size[1]*c <
            store.clevel.levelarea.coor[1][0]):
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
                              b.o_coor[0]+store.core.image[b.img].width],
                              [b.o_coor[1],
                              b.o_coor[1]+store.core.image[b.img].height]])
            if inarea(m_coor,button):
                b.press()
        Gui.killrcm()
    @staticmethod
    def killrcm():
        store.rcm.pop()
        store.rcm[0] = False
        store.core.store['spg'] = []
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
