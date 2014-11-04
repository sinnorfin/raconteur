# RACONTEUR V0.033
import pyglet
import math
import random
import os

import level
import player
import lists
import control

from pyglet.window import key
from pyglet.window import mouse
from pyglet import clock
from pyglet.gl import *
pyglet.resource.path = ['res']
pyglet.resource.reindex()
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, 
                GL_NEAREST)
class Game(object):
    def __init__(self):
        self.map_bt = pyglet.graphics.Batch()
        self.item_bt = pyglet.graphics.Batch()
        self.player_bt = pyglet.graphics.Batch()
        self.menu_bt = pyglet.graphics.Batch()
        self.debug_bt = pyglet.graphics.Batch()
        self.image = {}
        def center_tile(im): # puts anchor to image center
            im.anchor_x = im.width / 2
            im.anchor_y = im.height / 2
        for (file) in (os.listdir('res')):
            self.image[file.split('.')[0]] = pyglet.resource.image(file) 
            #creates pyglet images in self.image dictionary
            if file.split('_')[0] != 'c': 
                # centers images not beginning with 'c'
                center_tile(self.image[file.split('.')[0]])
        self.game_window = pyglet.window.Window(
                           self.gamesize_x * self.tilesize
                           +self.tilesize*3,
                           self.gamesize_y * self.tilesize
                           +self.tilesize,
                           resizable= False)
        self.xsize = self.game_window.width
        self.ysize = self.game_window.height
        clevel = level.level(self.image['space'].width)
        g_player = player.player(coor=[1,1],img='pchar',id=1)
        control = control.play()
        control.cplayer = lists.g_players[control.inturn]
        control.sp_topath = control.cplayer   
        control.goal = control.cplayer
        self.game_window.push_handlers(control.Play)
def getim(obj):
    return self.image[obj.img]
def inarea(m_coor,area):
    if (m_coor[0] >= area.coor[0][0] and
        m_coor[0] <= area.coor[0][1] and
        m_coor[1] >= area.coor[1][0] and
        m_coor[1] <= area.coor[1][1]):
        return True
def ontiles(m_coor,tiles):
    for tile in tiles:
        if (m_coor[0] >= clevel.ct(tile.coor[0])-self.anctile and
            m_coor[0] <= clevel.ct(tile.coor[0])+self.anctile and
            m_coor[1] >= clevel.ct(tile.coor[1])-self.anctile and
            m_coor[1] <= clevel.ct(tile.coor[1])+self.anctile):
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
class Button(object):
    def __init__(self,img,function=None):
        self.img = img
        self.o_coor = [0,0]
        self.function = function
    def drawbut(self,o_coor):
        self.o_coor = o_coor
        button = pyglet.sprite.Sprite(x=o_coor[0],y=o_coor[1],
                                      img=self.image[self.img], 
                                      bt = menu_batch)
        lists.sp_gui.append(button)
    def press(self):
        self.function()
        print 'you pressed %s' % self.img
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
        lists.sp_gui= []
class Cursor(object):
    def __init__(self):
        self.mposx = game.anctile
        self.mposy = game.anctile
        self.coor = [self.mposx,self.mposy]
        self.sp = pyglet.sprite.Sprite(x=self.mposx,
                                         y=self.mposy,
                             img=game.image['cursor'])   
        self.onarea = 'd'
class Tile(object): 
    def __init__(self, img, id=0, coor=[], passable= True,
                 occup= False, tt= 's',overlays=None,
                 functions=None,adjl=None,wadjl=None,rot=0):
        self.img = img
        self.coor = coor
        self.id = id
        self.passable = passable
        self.occup = occup
        self.tt = tt
        self.overlays = [] if overlays is None else overlays
        self.functions = [] if functions is None else functions
        self.dirs = {'xam':None,'xap':None,'yam':None,
                     'yap':None,'xym':None,'xyp':None,
                     'yxm':None,'yxp':None}
        self.adjl = [] if adjl is None else adjl
        self.wadjl = [] if wadjl is None else wadjl
        self.rot = rot
    def connect(self,ol=False,delete=False):
        #ol - limits connects to overlays
        #delete - removes sprite from list
        clist = None
        if ol == True:
            clist = lists.sp_overlays
        else: clist = lists.sp_tiles
        for sp_tile in clist:
            if sp_tile.id == self.id:
                if (ol == True and sp_tile.ol == True):
                    if delete == True:
                        clist.remove(sp_tile)
                    return sp_tile
                elif ol == False: 
                    if delete == True:
                        clist.remove(sp_tile)
                    return sp_tile
    def fnh_spaces(self,px,gx): #legk ures horiztile keresese
        horiz = []
        absval = []
        ind = 0
        c = ''
        clist = []
        dira = []
        dirb = []
        for g_tile in lists.g_tiles:
            if g_tile.y == self.y:
                if g_tile.tt == 'cse':
                    c = 'cse'
                    clist.append(g_tile)
                elif g_tile.tt == 'cnw':
                    c = 'cnw'
                    clist.append(g_tile)
                elif g_tile.tt == 'csw':
                    c = 'cnw'
                    clist.append(g_tile)
                elif g_tile.tt == 'cne':
                    c = 'cnw'
                    clist.append(g_tile)
        if len(clist) > 1:
            print 'MORE THAN ONE CORNER'
            for g_tile in clist:
                val = self.x - g_tile.x
                if val < 0:
                    dira.append(val)
                else:
                    dirb.append(val)
            if dira and dirb:
                print 'INVALID'
        for g_tile in lists.g_tiles:
            if self.tt == 'cse' or c == 'cse':
                if self.y == g_tile.y and self.id != g_tile.id and g_tile.x > self.x:
                    horiz.append(g_tile)
                    absval.append(abs(g_tile.x - self.x))
            elif self.tt == 'cnw' or c == 'cnw':
                if self.y == g_tile.y and self.id != g_tile.id and g_tile.x < self.x:
                    horiz.append(g_tile)
                    absval.append(abs(g_tile.x - self.x))
            else:
                if self.y == g_tile.y and self.id != g_tile.id :
                    horiz.append(g_tile)
                    absval.append(abs(g_tile.x - self.x))
        countmin = 0
        choice = []
        for val in absval:
            if val == min(absval):
                countmin +=1
        if countmin > 1:
            for g_tile in horiz:
                if abs(g_tile.x - self.x) == min(absval):
                    choice.append(g_tile)
            if px > gx or self.tt == 'cse':
                for g_tile in choice:
                    if g_tile.x > self.x:
                        return g_tile
            else:
                for g_tile in choice:
                    if g_tile.x < self.x:
                        return g_tile
        else: 
            ind = absval.index(min(absval))
        return horiz[ind]
    def fnv_spaces(self,py,gy): #legk ures vertitile keresese
        vert = []
        absval = []
        ind = 0
        c = ''
        clist = []
        dira = []
        dirb = []
        for g_tile in lists.g_tiles:
            if g_tile.y == self.y:
                if g_tile.tt == 'cse':
                    c = 'cse'
                    clist.append(g_tile)
                elif g_tile.tt == 'cnw':
                    c = 'cnw'
                    clist.append(g_tile)
                elif g_tile.tt == 'csw':
                    c = 'cnw'
                    clist.append(g_tile)
                elif g_tile.tt == 'cne':
                    c = 'cnw'
                    clist.append(g_tile)
        if len(clist) > 1:
            print 'MORE THAN ONE CORNER'
            for g_tile in clist:
                val = self.x - g_tile.x
                if val < 0:
                    dira.append(val)
                else:
                    dirb.append(val)
            if dira and dirb:
                print 'INVALID'
        for g_tile in lists.g_tiles:
            if self.x == g_tile.x and self.id != g_tile.id :
                vert.append(g_tile)
                absval.append(abs(g_tile.y - self.y))
        countmin = 0
        choice = []
        for val in absval:
            if val == min(absval):
                countmin +=1
        if countmin > 1:
            for g_tile in vert:
                if abs(g_tile.y - self.y) == min(absval):
                    choice.append(g_tile)
            if py > gy:
                for g_tile in choice:
                    if g_tile.y > self.y:
                        return g_tile
            else:
                for g_tile in choice:
                    if g_tile.y < self.y:
                        return g_tile
        else: 
            ind = absval.index(min(absval))
        return vert[ind]                
class Door(object):
    def __init__(self,func='door',loc=0, 
                 closed= False,locked = False):
        self.func = func
        self.loc = loc
        self.closed = closed
        self.locked = locked
    def use(self,loc):
        if self.closed == False:
            loc.img = 'door0'
            loc.passable = False
            loc.connect()._set_image(self.image['door0'])
            self.closed = True
        else: 
            if self.locked == False:
                loc.img = 'door1'
                loc.passable = True
                loc.connect()._set_image(self.image['door1'])
                self.closed = False
class SelBuild(object):
    def __init__(self):
        self.c = [0,False]
        self.blist = [['wall',0],['door0',0],['door1',0],['key',1]]
        self.label = pyglet.text.Label(self.blist[0][0],
                'Courier_new',30, x= game.game_window.width/2,
                y = game.gamesize_y * game.tilesize + 25,
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
                                        x= game.game_window.width/2,
                                        y = game.gamesize_y*game.tilesize+25,
                                        anchor_x = 'center',
                                        anchor_y = 'center')
    def build(self,type,gcoor,inid=0):
        buildloc = findtile(gcoor)
        scoor = [clevel.ct(gcoor[0]),
                 clevel.ct(gcoor[1])]
        if type != 'space' and buildloc.occup == True:
            type = 'none'
        if type == 'space':
            sp_built = Sp_Tile(x= scoor[0],
                               y= scoor[1],
                               img = game.image['space'],
                               bt = game.map_batch ,id= inid) 
            lists.sp_tiles.append(sp_built)
        if type == 'wall':
            var_wall = ['wall','wall_v1']
            buildloc.occup = True
            buildloc.passable = False
            buildloc.img = var_wall[random.randint(0,
                                    len(var_wall)-1)]
            buildloc.connect()._set_image(self.image[buildloc.img])
            buildloc.wadjl = level.adjlist(buildloc)
            level.arrange(buildloc) 
        if type == 'door0':
            buildloc.occup = True
            buildloc.passable = False
            door = Door(loc=buildloc,closed=True)
            buildloc.functions.append(door)
            buildloc.img = 'door0'
            buildloc.connect()._set_image(self.image['door0'])
            buildloc.wadjl = level.adjlist(buildloc)
            level.arrange(buildloc) 
        if type == 'door1':
            buildloc.occup = True
            buildloc.passable = True
            door = Door(loc=buildloc)
            buildloc.functions.append(door)
            buildloc.img = 'door1'
            buildloc.connect()._set_image(self.image['door1'])
            buildloc.wadjl = level.adjlist(buildloc)
            level.arrange(buildloc) 
    @staticmethod
    def overlay(type,coor,inid=0):
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
                sp_overlay = Sp_Tile(x=clevel.ct(key.x),y=clevel.ct(key.y),
                                     img=getim(key),
                                     bt=item_batch,id=key.id,
                                     ol=True) 
                lists.sp_overlays.append(sp_overlay)      
                Item.objid += 1
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
                             x =clevel.ct(Cursor.xcoor),
                             y =clevel.ct(Cursor.ycoor),
                             img = self.image['cursor'])          
                Cursor.mposx = Cursor.cursor.x 
                Cursor.mposy = Cursor.cursor.y 
                Cursor.coor = [Cursor.xcoor, Cursor.ycoor]
                Cursor.onarea = 'm'
                Path.clean_Path(tags=False)
                Path.goal = findtile(Cursor.coor)
                control.cplayer.pathing()
        return True
    @staticmethod
    def on_mouse_press(x,y,button,modifiers): 
        if button == mouse.LEFT: 
            if ontiles([x,y],Path.ptagged):
                Path.clean_Path()
                Path.goal = findtile(Cursor.coor)
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
class Sp_Tile(pyglet.sprite.Sprite):
    def __init__(self,id,ol=False,*args,**kwargs):
        pyglet.sprite.Sprite.__init__(self,*args,**kwargs)
        self.id = id
        self.ol = ol
class Typein(object):
    text =''
    firstt = True
    @staticmethod
    def on_text(text):
        if Typein.firstt == True and Typein.text == 't':
            Typein.text = ''
            Typein.firstt = False
        Typein.text += text
        if Typein.firstt != True: 
            Label.playername_label.text = Typein.text
        control.cplayer.name = Typein.text
    @staticmethod
    def on_key_press(symbol,modifiers):
        if symbol == key.ENTER:
            Label.playername_label.text = Typein.text
            Typein.text =''
            self.game_window.pop_handlers()
            control.handleraltered = False
        elif symbol == key.BACKSPACE:
            Typein.text = Typein.text[:-1]
            Label.playername_label.text = Typein.text
        elif symbol:
            return True

class Item(Tile):
    def __init__(self,id,x,y,img,name='',loc='',func=None):
        self.id = id
        self.x = x
        self.y = y
        self.img = img
        self.name = name
        self.loc = loc  
        self.func = func
    objid = 0 
class Spawn(object):
    reiterlist = []
    @staticmethod
    def g_object(num,type = ''):
        reiter = 0
        if type == 'wall':
            genloclist = []
            for genloc in lists.g_tiles:
                if genloc.occup == False:
                    genloclist.append(genloc)
            limit = len(genloclist)
            if num > limit: num = limit
            for i in range(num):
                genloc = genloclist[random.randint(0,len(genloclist)-1)]
                if genloc.occup == False :
                    SelBuild.build('wall',genloc.coor)
                else: reiter += 1
            if reiter != 0: 
                Spawn.g_object(reiter,type=type)
#Spawn.g_object(3,type = 'wall')
def det_ol(sp_tile):
    if sp_tile.ol:
        sp_tile.delete()
        return True
def dellevel(delol=False):
    if delol == True:
        lists.sp_overlays[:] = [ol for ol in List.sp_overlays if
                               not det_ol(ol)]
    for sp_tile in lists.sp_tiles:
        sp_tile.delete()
    del lists.sp_tiles[:]
    del lists.g_tiles[:]
def update(dt):
    if Path.anim == True:
        Anim.movetoward(Path.node.connect(),
                        control.cplayer.connect())
@self.game_window.event
def on_draw():
    self.game_window.clear()
    map_bt.draw()
    debug_bt.draw()
    item_bt.draw()
    player_bt.draw()
    SelBuild.build_label.draw()
    Cursor.cursor.draw()
    menu_bt.draw()
@self.game_window.event
def on_resize(width, height):
    self.tilesize
    self.anctile
    self.xsize
    self.ysize
    if width - 50 > self.xsize or width + 50 < self.xsize:
        scaleto = float(width) / float(self.xsize)
        scaletoint = scaleto*10000
        scaletoint = int(scaletoint)
        scaletoint = float(scaletoint)/10000
        glScalef(scaletoint, scaletoint, scaletoint)
        self.tilesize = self.tilesize * scaletoint
        self.anctile = self.tilesize/2
        Cursor.cursor.x = Cursor.cursor.x * scaletoint
        Cursor.cursor.y = Cursor.cursor.y * scaletoint
        #Cursor.mposx = Cursor.mposx * scaletoint
        #Cursor.mposy = Cursor.mposy * scaletoint
        self.xsize = width*scaletoint
        self.ysize = height*scaletoint
    width = self.xsize
    height = self.ysize
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, (1.0/30.0))
    game = Game()
    pyglet.app.run()
