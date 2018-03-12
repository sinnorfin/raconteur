import random
import pyglet.text
import store
import level
from sp import Sp_Tile

class SelBuild(object):
    def __init__(self,game_window):
        self.game_window = game_window
        self.c = [0,False]
        self.blist = [['wall',0],['door0',0],['door1',0],['key',1]]
        self.label = pyglet.text.Label(self.blist[0][0],
                'Courier_new',30, x= self.game_window.xcenter,
                y = self.game_window.y * store.ts + 25,
                anchor_x = 'center', anchor_y = 'center')
    def next(self):
        self.label.delete()
        buildnum = len(self.blist)
        self.c[0] +=1
        if self.c[0] == buildnum:
            self.c[0] = 0
        self.c[1] = self.blist[self.c[0]][1]
        self.label = pyglet.text.Label(
                                        self.blist[self.c[0]][0],
                                        'Courier_new',30,
                                        x= self.game_window.xcenter,
                                        y = self.game_window.y *
                                        self.game_window.ts+25,
                                        anchor_x = 'center',
                                        anchor_y = 'center')
    def build(self,buildloc,type,gcoor,inid=0):
        sp_built = None
        scoor = [store.ct(gcoor[0]),
                 store.ct(gcoor[1])]
        if type != 'space' and buildloc.occup == True:
            type = 'none'
        if type == 'space':
            sp_built = Sp_Tile(x= scoor[0],
                      y= scoor[1],
                      img = store.image['space'],
                      batch = store.map_bt ,id= inid)
            store.add(sp_built,'spt')
        if type == 'wall':
            var_wall = ['wall','wall_v1']
            buildloc.occup = True
            buildloc.passable = False
            buildloc.img = var_wall[random.randint(0,
                                    len(var_wall)-1)]
            buildloc.connect()._set_image(store.image[buildloc.img])
            buildloc.wadjl = level.adjlist(buildloc)
            level.arrange(buildloc)
        if type == 'door0':
            buildloc.occup = True
            buildloc.passable = False
            door = Door(loc=buildloc,closed=True)
            buildloc.functions.append(door)
            buildloc.img = 'door0'
            buildloc.connect()._set_image(store.image['door0'])
            buildloc.wadjl = level.adjlist(buildloc)
            level.arrange(buildloc)
        if type == 'door1':
            buildloc.occup = True
            buildloc.passable = True
            door = Door(loc=buildloc)
            buildloc.functions.append(door)
            buildloc.img = 'door1'
            buildloc.connect()._set_image(store.image['door1'])
            buildloc.wadjl = level.adjlist(buildloc)
            level.arrange(buildloc)
    @staticmethod
    def overlay(overloc,type,coor,inid=0):
        overloc = findtile(coor)
        lay = True
        for ol in overloc.overlays:
            if ol.name == type:
                lay = False
                delol(overloc,ol)
        if lay == True:
            if overloc.occup == True:
                type = 'none'
            overloc.occup = True
            if type == 'key':
                key = Item(id=Item.objid, x=coor[0], y=coor[1],
                           img='key',name='key',
                           loc=overloc,func='item_p')
                overloc.overlays.append(key)
                sp_overlay = Sp_Tile(x=store.ct(key.x),y=store.ct(key.y),
                                     img=getim(key),
                                     batch=store.item_bt,id=key.id,
                                     ol=True)
                sp_overlays.append(sp_overlay)
                Item.objid += 1
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
        self.mposx = store.ats
        self.mposy = store.ats
        self.coor = [self.mposx,self.mposy]
        self.sp = pyglet.sprite.Sprite(x=self.mposx,
                                       y=self.mposy,
                                     img=store.image['cursor'])
        self.onarea = 'd'
