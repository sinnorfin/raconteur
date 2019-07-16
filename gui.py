import random
import pyglet.text
import store
import level
import element
import label
import pdb


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
                                      img=store.image[self.img],
                                      batch = store.menu_bt)
        store.store['spg'].append(button)
    def press(self):
        self.function()
        print ('you pressed %s' % self.img)
class Frame(object):
    def __init__(self,o_coor,clickloc):
            self.o_coor = o_coor
            self.clickloc = clickloc
            self.orig = [0,0]
            self.size = [80,50]
            self.buttons = []
    def add_buttons(self,source):
        for elem in source:
            for button in elem.buttons:
                self.buttons.append(Button(button[0],button[1]))
    def fitmenu(self,c):
        fitx = (self.o_coor[0]+self.size[0] >
                store.clevel.levelarea.coor[0][1])
        fity = (self.o_coor[1]-self.size[1]*c <
                store.clevel.levelarea.coor[1][0])
        if fitx and fity:
            self.o_coor[0] -= self.size[0]
            self.o_coor[1] -= self.size[1]*c
        elif fitx:
            self.o_coor[0] -= self.size[0]
        elif fity:
            self.o_coor[1] += self.size[1]*c
        self.orig = self.o_coor
    def refresh_menu(self):
        self.rcmhead.drawbut([self.orig[0],self.orig[1] - 50])
        for b in self.buttons:
            b.drawbut([self.orig[0],self.orig[1] - 100 -
                      self.buttons.index(b)*self.size[1]])
    def click(self,m_coor):
        for b in self.buttons:
            button = level.Gamearea(coor=[[b.o_coor[0],
                              b.o_coor[0]+store.image[b.img].width],
                              [b.o_coor[1],
                              b.o_coor[1]+store.image[b.img].height]])
            if inarea(m_coor,button):
                b.press()
        self.killrcm()
    def killrcm(self):
        store.rcm.pop()
        store.rcm[0] = False
        store.store['spg'] = []
class Rightclickmenu(Frame):
    def __init__(self,o_coor,clickloc):
        super(Rightclickmenu, self).__init__(o_coor,clickloc)
        self.orig = [0,0]
        self.size = [80,50]
        self.buttons = []
        self.rcmhead = Button('c_menu')
        if store.cursor.onarea == 'l':
                store.rcm[0] = True
                self.rightclickmenu()
    def rightclickmenu(self):
        if self.clickloc in store.cplayer.loc.adjl:
            self.add_buttons(self.clickloc.functions)
        if self.clickloc is store.cplayer.loc:
            self.add_buttons(self.clickloc.overlays)
            self.add_buttons(store.cplayer.inv)
        self.fitmenu(len(self.buttons)+1)
        self.refresh_menu()
class Textbox(Frame):
    def __init__(self,o_coor,clickloc,text):
        super(Textbox, self).__init__(o_coor,clickloc)
        self.text = text
        self.rcmhead = Button('c_menu')
        self.size = [0,0]
        self.display()
    def display(self):
        text = pyglet.text.Label(self.text,
                                'Courier_new',14,
                                x= self.o_coor[0],
                                y = self.o_coor[1],
                                anchor_x = 'left',
                                anchor_y = 'center',
                                batch = store.menu_bt)
class Cursor(object):
    def __init__(self):
        self.mposx = store.ats
        self.mposy = store.ats
        self.coor = [self.mposx,self.mposy]
        self.sp = pyglet.sprite.Sprite(x=self.mposx,
                                       y=self.mposy,
                                     img=store.image['cursor'])
        self.onarea = 'd'
