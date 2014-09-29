# RACONTEUR V0.03
import pyglet
import math
import cPickle
import random
import os
from pyglet.window import key
from pyglet.window import mouse
from pyglet import clock
from pyglet.gl import *
pyglet.resource.path = ['res']
pyglet.resource.reindex()

ROOMSIZEX = 20
ROOMSIZEY = 15
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

map_batch = pyglet.graphics.Batch()
item_batch = pyglet.graphics.Batch()
player_batch = pyglet.graphics.Batch()
menu_batch = pyglet.graphics.Batch()
debug_batch = pyglet.graphics.Batch()
IMAGE = {}
def center_tile(im): # puts anchor to image center
    im.anchor_x = im.width / 2
    im.anchor_y = im.height / 2
for (file) in (os.listdir('res')):
    IMAGE[file.split('.')[0]] = pyglet.resource.image(file) 
    #creates pyglet images in IMAGE dictionary
    if file.split('_')[0] != 'c': 
        # centers anchor of images not beginning with 'c'
        center_tile(IMAGE[file.split('.')[0]])
TILESIZE = IMAGE['space'].width
ANC_TILE = TILESIZE / 2
GAME_WINDOW = pyglet.window.Window(ROOMSIZEX * TILESIZE+TILESIZE*3,
                                   ROOMSIZEY * TILESIZE+TILESIZE,
                                   resizable= True)
XSIZE = GAME_WINDOW.width
YSIZE = GAME_WINDOW.height
def getim(tile):
    return IMAGE[tile.img]
def findtile(coor):
    for g_tile in List.g_tiles:
        if (g_tile.coor == coor):
            return g_tile
def inarea(m_coor,area):
    if (m_coor[0] >= area.coor[0][0] and
        m_coor[0] <= area.coor[0][1] and
        m_coor[1] >= area.coor[1][0] and
        m_coor[1] <= area.coor[1][1]):
        return True
def ontiles(m_coor,tiles):
    for tile in tiles:
        if (m_coor[0] >= ct(tile.coor[0])-ANC_TILE and
            m_coor[0] <= ct(tile.coor[0])+ANC_TILE and
            m_coor[1] >= ct(tile.coor[1])-ANC_TILE and
            m_coor[1] <= ct(tile.coor[1])+ANC_TILE):
            return True
def delol(overloc,ol):
    ol.connect(True,delete=True).delete()
    overloc.overlays.remove(ol)
    if len(overloc.overlays) == 0:
        overloc.occup = False
class List(object):
    g_tiles = []
    g_players = []
    sp_overlays = []
    sp_tiles = []
    sp_gui = []
def prange(loc):
    range = Control.CurrentPlayer.distance(loc)
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
class Gamearea(object):
    def __init__(self,id=None,name=None,coor=None):
        self.id = id
        self.name = name
        self.coor = coor
class Button(object):
    def __init__(self,img,function=None):
        self.img = img
        self.o_coor = [0,0]
        self.function = function
    def drawbut(self,o_coor):
        self.o_coor = o_coor
        button = pyglet.sprite.Sprite(x=o_coor[0],y=o_coor[1],
                                      img=IMAGE[self.img], 
                                      batch = menu_batch)
        List.sp_gui.append(button)
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
            Mapengine.levelarea.coor[0][1]):
            fitx = True
        if (self.o_coor[1]-self.size[1]*c < 
            Mapengine.levelarea.coor[1][0]): 
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
            button = Gamearea(coor=[[b.o_coor[0],
                              b.o_coor[0]+IMAGE[b.img].width],
                              [b.o_coor[1],
                              b.o_coor[1]+IMAGE[b.img].height]])
            if inarea(m_coor,button):
                b.press()
        Gui.killrcm()
    @staticmethod
    def killrcm():
        Gui.rcm.pop()
        Gui.rcm[0] = False
        List.sp_gui= []
class Cursor(object):
    mposx = ANC_TILE
    mposy = ANC_TILE
    coor = [mposx,mposy]
    cursor = pyglet.sprite.Sprite(x= mposx, y= mposy, 
                                  img = IMAGE['cursor'])   
    onarea = 'd'
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
            clist = List.sp_overlays
        else: clist = List.sp_tiles
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
        for g_tile in List.g_tiles:
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
        for g_tile in List.g_tiles:
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
        for g_tile in List.g_tiles:
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
        for g_tile in List.g_tiles:
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
            loc.connect()._set_image(IMAGE['door0'])
            self.closed = True
        else: 
            if self.locked == False:
                loc.img = 'door1'
                loc.passable = True
                loc.connect()._set_image(IMAGE['door1'])
                self.closed = False
class SelBuild(object):
    c = [0,False]
    buildlist = [['wall',0],['door0',0],['door1',0],['key',1]]
    build_label = pyglet.text.Label(buildlist[0][0], 'Courier_new',
                                    30,x= GAME_WINDOW.width/2,
                                    y = ROOMSIZEY*TILESIZE+25,
                                    anchor_x = 'center',
                                    anchor_y = 'center')
    @staticmethod
    def next():
        SelBuild.build_label.delete()
        buildnum = len(SelBuild.buildlist)
        SelBuild.c[0] +=1
        if SelBuild.c[0] == buildnum:
            SelBuild.c[0] = 0
        SelBuild.c[1] = SelBuild.buildlist[SelBuild.c[0]][1]
        SelBuild.build_label = pyglet.text.Label(
                                        SelBuild.buildlist[SelBuild.c[0]][0], 
                                        'Courier_new',30,
                                        x= GAME_WINDOW.width/2,
                                        y = ROOMSIZEY*TILESIZE+25,
                                        anchor_x = 'center',
                                        anchor_y = 'center')
    @staticmethod
    def build(type,gcoor,inid=0):
        buildloc = findtile(gcoor)
        scoor = [ct(gcoor[0]),
                 ct(gcoor[1])]
        if type != 'space' and buildloc.occup == True:
            type = 'none'
        if type == 'space':
            sp_built = Sp_Tile(x= scoor[0],
                               y= scoor[1],
                               img = IMAGE['space'],
                               batch = map_batch ,id= inid) 
            List.sp_tiles.append(sp_built)
        if type == 'wall':
            var_wall = ['wall','wall_v1']
            buildloc.occup = True
            buildloc.passable = False
            buildloc.img = var_wall[random.randint(0,
                                    len(var_wall)-1)]
            buildloc.connect()._set_image(IMAGE[buildloc.img])
            buildloc.wadjl = Mapengine.adjlist(buildloc)
            Mapengine.arrange(buildloc) 
        if type == 'door0':
            buildloc.occup = True
            buildloc.passable = False
            door = Door(loc=buildloc,closed=True)
            buildloc.functions.append(door)
            buildloc.img = 'door0'
            buildloc.connect()._set_image(IMAGE['door0'])
            buildloc.wadjl = Mapengine.adjlist(buildloc)
            Mapengine.arrange(buildloc) 
        if type == 'door1':
            buildloc.occup = True
            buildloc.passable = True
            door = Door(loc=buildloc)
            buildloc.functions.append(door)
            buildloc.img = 'door1'
            buildloc.connect()._set_image(IMAGE['door1'])
            buildloc.wadjl = Mapengine.adjlist(buildloc)
            Mapengine.arrange(buildloc) 
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
                sp_overlay = Sp_Tile(x=ct(key.x),y=ct(key.y),
                                     img=getim(key),
                                     batch=item_batch,id=key.id,
                                     ol=True) 
                List.sp_overlays.append(sp_overlay)      
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
            GAME_WINDOW.pop_handlers()
            Control.handleraltered = False
            Path.clean_Path()
            del Path.ptagged[:]
            return True
    @staticmethod
    def on_mouse_motion(x,y,dx,dy):
        if (x+ANC_TILE > Cursor.mposx + TILESIZE or
            x+ANC_TILE < Cursor.mposx or 
            y+ANC_TILE > Cursor.mposy + TILESIZE or 
            y+ANC_TILE < Cursor.mposy ):
            if ontiles([x,y],Path.ptagged):
                Cursor.xcoor = math.floor(x/TILESIZE)
                Cursor.ycoor = math.floor(y/TILESIZE)
                Cursor.cursor = pyglet.sprite.Sprite( 
                             x =ct(Cursor.xcoor),
                             y =ct(Cursor.ycoor),
                             img = IMAGE['cursor'])          
                Cursor.mposx = Cursor.cursor.x 
                Cursor.mposy = Cursor.cursor.y 
                Cursor.coor = [Cursor.xcoor, Cursor.ycoor]
                Cursor.onarea = 'm'
                Path.clean_Path(tags=False)
                Path.goal = findtile(Cursor.coor)
                Control.CurrentPlayer.pathing()
        return True
    @staticmethod
    def on_mouse_press(x,y,button,modifiers): 
        if button == mouse.LEFT: 
            if ontiles([x,y],Path.ptagged):
                Path.clean_Path()
                Path.goal = findtile(Cursor.coor)
                Control.CurrentPlayer.pathing()
                Control.CurrentPlayer.pmove(Path.cpath.nodes,
                                            Path.step)
                del Path.ptagged[:]
                Path.clean_Path()
                GAME_WINDOW.pop_handlers()
                Control.handleraltered = False
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
            Control.CurrentPlayer.pmove(Path.cpath.nodes,Path.step)
        if animated.x < goal.x:
            Control.CurrentPlayer.look = 'pchar'
            animated._set_image(IMAGE[Control.CurrentPlayer.look])
            animated.x += 10
        if animated.y < goal.y:
            Control.CurrentPlayer.look = 'pcharB'
            animated._set_image(IMAGE[Control.CurrentPlayer.look])
            animated.y += 10
        if animated.x > goal.x:
            Control.CurrentPlayer.look = 'pcharR'
            animated._set_image(IMAGE[Control.CurrentPlayer.look])
            animated.x -= 10
        if animated.y > goal.y:
            Control.CurrentPlayer.look = 'pcharF'
            animated._set_image(IMAGE[Control.CurrentPlayer.look])
            animated.y -= 10   
class Control(object):  
    waypoint = False
    CurrentPlayer = ''
    sp_topath = ''
    goal = ''
    goalwp = ''
    obstacles = []
    distances = []
    xlist = []
    ylist = []
    handleraltered = False
    @staticmethod
    def pushhandlers(Class):
        if Control.handleraltered == True:
            GAME_WINDOW.pop_handlers()
            Control.handleraltered = False
        GAME_WINDOW.push_handlers(Class)
        Control.handleraltered = True
    def __init__(self):
        self.inturn = 0     
    def turn(self):
        self.inturn += 1
        playnum = len(List.g_players)
        if Control.inturn == playnum:
            Control.inturn = 0
        Control.CurrentPlayer = List.g_players[Control.inturn]
        Labels.create(Control.CurrentPlayer.name, 
                      Labels.playername_label)
    def on_key_press(self,symbol,modifiers):
        if symbol == key.UP:
            Control.CurrentPlayer.moveup()          
        elif symbol == key.DOWN:
            Control.CurrentPlayer.movedown()
        elif symbol == key.LEFT:
            Control.CurrentPlayer.moveleft()
        elif symbol == key.RIGHT:
            Control.CurrentPlayer.moveright()
        elif symbol == key.SPACE:
            if not Control.CurrentPlayer.cols():
                if Control.CurrentPlayer.img == 'pchar':
                    Control.CurrentPlayer.connect()._set_image(
                                             IMAGE['pchar_1b'])
                    Control.CurrentPlayer.img = 'pchar_1b'
                else: 
                    Control.CurrentPlayer.connect()._set_image(
                                                IMAGE['pchar'])
                    Control.CurrentPlayer.img = 'pchar'
                self.turn()
        elif symbol == key.B:
            if not Control.CurrentPlayer.cols():
                if SelBuild.c[1] == 1:
                    SelBuild.overlay(SelBuild.buildlist[
                                     SelBuild.c[0]][0],
                            Control.CurrentPlayer.coor,
                            findtile(Control.CurrentPlayer))
                    self.turn()
                else:
                    SelBuild.build(SelBuild.buildlist[
                                        SelBuild.c[0]][0],
                            Control.CurrentPlayer.coor,
                            findtile(Control.CurrentPlayer))
                    self.turn()
        elif symbol == key.P:
            Control.CurrentPlayer.addplayer()
        elif symbol == key.DELETE:
            dellevel(delol=True)
            Mapengine.levelgen()
        elif symbol == key.R:
            dellevel(delol=True)
            Mapengine.levelgen()
            Spawn.g_object(8,type = 'wall')
        elif symbol == key.S:
            savelevel()
        elif symbol == key.L:
            loadlevel()
        elif symbol == key.Q:
            SelBuild.next()
        elif symbol == key.O:
            print len(Control.CurrentPlayer.player_bordering())
        elif symbol == key.T:
            Control.pushhandlers(Typein)
            Typein.firstt = True
        elif symbol == key.M:
            Control.pushhandlers(Path)
            Control.CurrentPlayer.moveg()
    def on_mouse_motion(self,x,y,dx,dy):
        if (x+ANC_TILE > Cursor.mposx + TILESIZE or
            x+ANC_TILE < Cursor.mposx or 
            y+ANC_TILE > Cursor.mposy + TILESIZE or 
            y+ANC_TILE < Cursor.mposy ):
            if inarea([x,y],Mapengine.levelarea):
                Cursor.xcoor = math.floor(x/TILESIZE)
                Cursor.ycoor = math.floor(y/TILESIZE)
                Cursor.cursor = pyglet.sprite.Sprite( 
                             x =ct(Cursor.xcoor),
                             y =ct(Cursor.ycoor),
                             img = IMAGE['cursor'])          
                Cursor.mposx = Cursor.cursor.x 
                Cursor.mposy = Cursor.cursor.y 
                Cursor.coor = [Cursor.xcoor, Cursor.ycoor]
                Cursor.onarea = 'l'
            else: Cursor.onarea = 'o'
    def on_mouse_press(self,x,y,button,modifiers): 
        clickloc = findtile(Cursor.coor)
        if button == mouse.LEFT:
            if (Gui.rcm[0] and inarea(Cursor.coor,
                Mapengine.levelarea)): 
                Gui.rcm[1].click([x,y])
            elif (not Gui.rcm[0] and inarea(Cursor.coor,
                Mapengine.levelarea)):
                for func in clickloc.functions:
                    if (func.func == 'door' and
                        Mapengine.adj(Control.CurrentPlayer,
                                      clickloc)):
                            func.use(clickloc)
            #elif List.g_tiles:
                #for g_tile in List.g_tiles:
                    #if Cursor.coor == g_tile.coor: 
                        #if not Mapengine.standon(
                            #Control.CurrentPlayer, g_tile):
                                #Control.pathto(
                                    #Control.CurrentPlayer,g_tile)
        elif button == mouse.RIGHT:
            if inarea([x,y],Mapengine.levelarea):
                print 'MENNU'
                if Gui.rcm[0]:
                   Gui.killrcm() 
                rcm = Gui([x,y],'rcm',clickloc)
                Gui.rcm.append(rcm)
            else: print 'NOMENU'
        elif button == mouse.MIDDLE:
            print len(clickloc.functions)
class Sp_Tile(pyglet.sprite.Sprite):
    def __init__(self,id,ol=False,*args,**kwargs):
        pyglet.sprite.Sprite.__init__(self,*args,**kwargs)
        self.id = id
        self.ol = ol
def ct(tile):
    tiled = (tile*TILESIZE)+ANC_TILE
    return tiled
class Player(object):   
    cid = 2 
    def __init__(self, coor, img, id=0,name = 'Player',
                 inv=None):
        self.coor = coor 
        self.img = img
        self.id = id
        self.loc = findtile(self.coor) 
        self.name = name
        self.inv = [] if inv is None else inv
        self.itemcount = 0
        self.look = 'pchar'
        self.mrange = 15
    def connect(self):
        for sp_overlay in List.sp_overlays:
            if (sp_overlay.id == self.id and 
               not sp_overlay.ol):
                return sp_overlay
    def cols(self):
        collision = False
        for g_tile in List.g_tiles:
            if (g_tile.passable == False and 
                g_tile.coor == self.coor):
                    collision = True
            else:collision = False
        return collision
    def distance(self,target):
        distance = [abs(self.coor[0]-target.coor[0]),
                    abs(self.coor[1]-target.coor[1])]
        return distance
    def player_bordering(self): #searches for spaces around player
        player_bordering = []   #could be extended to find whatever around player
        up = self.coor[1] + 1
        down = self.coor[1] - 1
        right = self.coor[0] + 1
        left = self.coor[0] - 1
        for g_tile in List.g_tiles:
            add = False
            if (g_tile.coor[1] == up and 
                g_tile.coor[0] == right):
                    add = True
                    ckcoll = [up,right]
            elif (g_tile.coor[1] == down and
                  g_tile.coor[0] == left): 
                    add = True
                    ckcoll = [down,left]
            elif (g_tile.coor[1] == up and
                  g_tile.coor[0] == left):
                    add = True
                    ckcoll = [up,left]
            elif (g_tile.coor[1] == down and
                  g_tile.coor[0] == right):
                    add = True
                    ckcoll = [down,right]
            elif (g_tile.coor[1] == up and 
                  g_tile.coor[0] == self.coor[0]):
                    add = True
                    ckcoll = [up,self.coor[0]]
            elif (g_tile.coor[1] == down and 
                  g_tile.coor[0] == self.coor[0]):
                    add = True
                    ckcoll = [down,self.coor[0]]
            elif (g_tile.coor[1] == self.coor[1] and 
                  g_tile.coor[0] == right):
                    add = True
                    ckcoll = [self.coor[1],right]
            elif (g_tile.coor[1] == self.coor[1] and 
                  g_tile.coor[0] == left):
                    add = True
                    ckcoll = [self.coor[1],left]
            if (add == True and
                Mapengine.coll([ckcoll[0],ckcoll[1]]) == False): 
                    player_bordering.append(g_tile)
        return player_bordering 
    def pathing(self):
        self.checkmv(self.loc,True,pat=True)
        Path.tagged = list(set(Path.tagged))
        if Path.pl:
            mincost = Path.pl[0].cost
            costlist=[]
            for path in Path.pl:
                costlist.append(path.cost)
            Path.cpath = Path.pl[costlist.index(min(costlist))]
            for node in Path.cpath.nodes:
                tag = pyglet.sprite.Sprite(x= ct(node.coor[0]),
                              y= ct(node.coor[1]),
                              img = IMAGE['marker2'],
                              batch = debug_batch)   
                Path.wp.append(tag)
    def moveg(self):
        Path.clean_Path()
        self.checkmv(self.loc,True)        
        Path.tagged = list(set(Path.tagged))
        for tile in Path.tagged:
            tag = pyglet.sprite.Sprite(x= ct(tile.coor[0]),
                          y= ct(tile.coor[1]),
                          img = IMAGE['marker'],
                          batch = debug_batch)   
            Path.tags.append(tag)
        for tagged in Path.tagged:
            Path.ptagged.append(tagged)
        if ontiles([Cursor.mposx,Cursor.mposy],Path.ptagged):
            Path.clean_Path(tags=False)
            Path.goal = findtile(Cursor.coor)
            Control.CurrentPlayer.pathing()
    def checkmv(self,tchk,first = False,pat=False,f=None):  
        checkdirs = [tchk.dirs['xam'],tchk.dirs['xap'],
                     tchk.dirs['yam'],tchk.dirs['yap']]
        if f: checkdirs.pop(checkdirs.index(f))
        if first == True:
            st_cost = Path.cost
            st_tagged = len(Path.tagged)
            for ccheck in checkdirs:
                Path.cost = st_cost
                for i in range(len(Path.tagged)-st_tagged):
                    if pat==True:Path.tagged.pop()
                if pat == True:
                    self.checkmv(ccheck,pat=True,
                                 f=tchk)
                else:
                    self.checkmv(ccheck,f=tchk)
        if (first == False and tchk.passable == True and
            Path.cost + 1 <= self.mrange):
            Path.cost += 1
            Path.tagged.append(tchk)
            st_cost = Path.cost
            st_tagged = len(Path.tagged)
            if pat == True and tchk.coor == Path.goal.coor:
                p = Path(Path.cost,[])
                for node in Path.tagged: p.nodes.append(node)
                Path.pl.append(p) 
            if Path.cost != self.mrange:
                for ccheck in checkdirs:
                    Path.cost = st_cost
                    for i in range(len(Path.tagged)-st_tagged):
                        if pat == True:Path.tagged.pop()
                    if pat == True:
                        self.checkmv(ccheck,pat=True,
                                     f=tchk)
                    else:
                        self.checkmv(ccheck,f=tchk)
    def moveup(self):
        if not Mapengine.coll([self.coor[1]+1,self.coor[0]]):
            self.coor[1] += 1
            self.look = 'pcharB'
            self.connect()._set_image(IMAGE[self.look])
            self.connect().y = ct(self.coor[1])
            self.loc = findtile(self.coor)
            Control.turn()
    def movedown(self):
        if not Mapengine.coll([self.coor[1]-1,self.coor[0]]):
            self.coor[1] -= 1
            self.look = 'pcharF'
            self.connect()._set_image(IMAGE[self.look])
            self.connect().y = ct(self.coor[1])
            self.loc = findtile(self.coor)
            Control.turn()
    def moveleft(self):
        if not Mapengine.coll([self.coor[1],self.coor[0]-1]):
            self.coor[0] -= 1 
            self.look = 'pcharR'
            self.connect()._set_image(IMAGE[self.look])
            self.connect().x = ct(self.coor[0])
            self.loc = findtile(self.coor)
            Control.turn()
    def moveright(self):
        if not Mapengine.coll([self.coor[1],self.coor[0]+1]):
            self.coor[0] += 1
            self.look = 'pchar'
            self.connect()._set_image(IMAGE[self.look])
            self.connect().x = ct(self.coor[0])
            self.loc = findtile(self.coor)
            Control.turn()
    def pmove(self,path,step):
        if Path.step < len(path):
            Path.node = path[step]
            Path.anim = True 
        else: 
            Path.step = 0
            self.coor[0] = Path.goal.coor[0]
            self.coor[1] = Path.goal.coor[1]
            self.loc = findtile(self.coor)
            self.connect().x = ct(self.coor[0])
            self.connect().y = ct(self.coor[1])
            Control.turn()
    def addplayer(self):
        g_newplayer = Player(coor=[self.coor[0]+1,self.coor[1]+1], 
                             img='pchar',id=Player.cid)
        Player.cid +=1
        sp_newplayer = Sp_Tile (x=ct(g_newplayer.coor[0]), 
                                y=ct(g_newplayer.coor[1]), 
                                img = getim(g_newplayer),
                                id=g_newplayer.id,
                                batch = player_batch)
        List.g_players.append(g_newplayer)
        List.sp_overlays.append(sp_newplayer)
class Mapengine(object):
    @staticmethod
    def adj(tocheck, against):
        if (against.coor[0] == tocheck.coor[0] + 1 and 
            against.coor[1] == tocheck.coor[1] or
            against.coor[0] == tocheck.coor[0] - 1 and 
            against.coor[1] == tocheck.coor[1] or
            against.coor[1] == tocheck.coor[1] + 1 and
            against.coor[0] == tocheck.coor[0] or
            against.coor[1] == tocheck.coor[1] - 1 and 
            against.coor[0] == tocheck.coor[0]) :
            adj = True
        else: adj = False
        return adj
    @staticmethod
    def adjlist(tocheck):
        adjlist = []
        for g_tile in tocheck.dirs.itervalues():
            if g_tile and g_tile.passable == False:
                adjlist.append(g_tile)
        for g_tile in tocheck.dirs.itervalues():
            if g_tile and g_tile.passable == False: 
                adjlist.append(g_tile)
        return adjlist
    @staticmethod
    def arrange(toarrange,fit=True):
        toarrange.connect()._set_rotation(0)
        toarrange.rot = 0
        xac = 0
        yac = 0
        if (toarrange.dirs['xam'] and 
            toarrange.dirs['xam'].passable == False): 
            xac= xac+1 
        if (toarrange.dirs['xap'] and 
            toarrange.dirs['xap'].passable == False): 
            xac= xac+1 
        if (toarrange.dirs['yam'] and 
            toarrange.dirs['yam'].passable == False): 
            yac= yac+1 
        if (toarrange.dirs['yap'] and 
            toarrange.dirs['yap'].passable == False): 
            yac= yac+1 
        if xac == 0 and yac == 0:
            toarrange.connect()._set_image(IMAGE['pil'])
            toarrange.img = 'pil'
            toarrange.tt = 's'
        elif xac == 1 and yac == 0:
            if (toarrange.dirs['xap'] and
                toarrange.dirs['xap'].passable == False):
                toarrange.connect()._set_image(IMAGE['cap'])
                toarrange.connect()._set_rotation(270)
                toarrange.img = 'cap'
                toarrange.tt = 'xm_c'
                toarrange.rot = 270
            elif (toarrange.dirs['xam'] and 
                toarrange.dirs['xam'].passable == False):
                toarrange.connect()._set_image(IMAGE['cap'])
                toarrange.connect()._set_rotation(90)
                toarrange.img = 'cap'
                toarrange.tt = 'xp_c'
                toarrange.rot = 90
        elif xac == 2 and yac == 0 :
            toarrange.connect()._set_rotation(90)
            toarrange.tt = 'x'
            toarrange.connect()._set_image(IMAGE['wall'])
            toarrange.img = 'wall'
            toarrange.rot = 90
        elif xac != 0 and yac != 0:
            if xac+yac == 2:
                toarrange.connect()._set_image(IMAGE['corner'])
                toarrange.img = 'corner'
                if ((toarrange.dirs['xap'] and 
                    toarrange.dirs['yam']) and
                    (toarrange.dirs['xap'].passable == False and
                    toarrange.dirs['yam'].passable == False)):
                    toarrange.connect()._set_rotation(0)
                    toarrange.tt = 'cse'
                    toarrange.rot = 0
                elif ((toarrange.dirs['xam'] and 
                    toarrange.dirs['yam']) and
                    (toarrange.dirs['xam'].passable == False and
                    toarrange.dirs['yam'].passable == False)):
                    toarrange.connect()._set_rotation(90)
                    toarrange.tt = 'csw'
                    toarrange.rot = 90
                elif ((toarrange.dirs['xam'] and 
                    toarrange.dirs['yap']) and
                    (toarrange.dirs['xam'].passable == False and
                    toarrange.dirs['yap'].passable == False)):
                    toarrange.connect()._set_rotation(180)
                    toarrange.tt = 'cnw'
                    toarrange.rot = 180
                else:   
                    toarrange.connect()._set_rotation(270)
                    toarrange.tt = 'cne'
                    toarrange.rot = 270
            elif xac+yac == 3:
                toarrange.connect()._set_image(IMAGE['tsect'])
                toarrange.img = 'tsect'
                if (not toarrange.dirs['xam'] or
                    toarrange.dirs['xam'].passable == True):
                    toarrange.connect()._set_rotation(0)
                    toarrange.tt = 'tw'
                    toarrange.rot = 0
                elif (not toarrange.dirs['yap'] or
                    toarrange.dirs['yap'].passable == True):
                    toarrange.connect()._set_rotation(90)
                    toarrange.tt = 'tn'
                    toarrange.rot = 90
                elif (not toarrange.dirs['xap'] or
                    toarrange.dirs['xap'].passable == True):
                    toarrange.connect()._set_rotation(180)
                    toarrange.tt = 'te'
                    toarrange.rot = 180
                else: 
                    toarrange.connect()._set_rotation(270)
                    toarrange.tt = 'ts'
                    toarrange.rot = 270
            else:
                toarrange.connect()._set_image(IMAGE['fourway'])
                toarrange.img = 'fourway'
                toarrange.tt = 'fw'
        else: 
            if (yac == 1 and toarrange.dirs['yam'] and 
                toarrange.dirs['yam'].passable == False):
                toarrange.connect()._set_image(IMAGE['cap'])
                toarrange.connect()._set_rotation(0)
                toarrange.img = 'cap'
                toarrange.tt = 'xp_c'
                toarrange.rot = 0
            elif (yac == 1 and toarrange.dirs['yap'] and 
                toarrange.dirs['yap'].passable == False):
                toarrange.connect()._set_image(IMAGE['cap'])
                toarrange.connect()._set_rotation(180)
                toarrange.img = 'cap'
                toarrange.tt = 'xm_c'
                toarrange.rot = 180
            else:
                toarrange.tt = 'y'
                toarrange.connect()._set_image(IMAGE['wall'])
                toarrange.img = 'wall'
        if fit == True:
            Mapengine.fitnext(toarrange.wadjl)
    @staticmethod   
    def coll(direc):
        collision = False
        for g_tile in List.g_tiles:
            if (g_tile.passable == False and
                g_tile.coor[1] == direc[0] and g_tile.coor[0] == direc[1]):
                    collision = True
                    return collision
        return collision
    @staticmethod
    def fitnext(tile):
        for i in tile:
            i.wadjl = Mapengine.adjlist(i)
            Mapengine.arrange(i,False)
    @staticmethod
    def levelgen(): 
        if List.sp_tiles: dellevel()
        Mapengine.levelarea = Gamearea(1,'level',
                             [[0,TILESIZE*ROOMSIZEX],
                             [0,TILESIZE*ROOMSIZEY]])
        gcoor = [0,0]
        genid = 1
        for i in range(ROOMSIZEX):
            Mapengine.ctile(gcoor,genid)
            genid +=1   
            for i in range(ROOMSIZEY-1):
                gcoor= [gcoor[0],gcoor[1] + 1]
                Mapengine.ctile(gcoor,genid)
                genid += 1
            gcoor= [gcoor[0],0]
            gcoor= [gcoor[0]+1,gcoor[1]]
        for tile in List.g_tiles:
            Mapengine.interlace(tile)
            SelBuild.build('space',tile.coor,tile.id)  
            if len(tile.adjl) != 8:
                SelBuild.build('wall',tile.coor)
    @staticmethod
    def ctile(gcoor,genid):
        var_space = ['space','space_v1','space','space_v2','space_v3']
        g_gen = Tile(img=var_space[random.randint(0,
                       len(var_space)-1)],
                       id=genid,coor=gcoor,occup=False)  
        List.g_tiles.append(g_gen)
    @staticmethod
    def interlace(tile):
        for check in List.g_tiles:
            if (tile.coor[0] == check.coor[0] and
                abs(check.coor[1]-tile.coor[1]) == 1):
                if check.coor[1]-tile.coor[1] == -1:
                    tile.dirs['yam'] = check
                    tile.adjl.append(check)
                else: 
                    tile.dirs['yap'] = check
                    tile.adjl.append(check)
            elif (tile.coor[1] == check.coor[1] and
                  abs(check.coor[0]-tile.coor[0]) == 1):
                if check.coor[0]-tile.coor[0] == -1:
                    tile.dirs['xam'] = check
                    tile.adjl.append(check)
                else: 
                    tile.dirs['xap'] = check
                    tile.adjl.append(check)
            else:
                if (abs(check.coor[0]-tile.coor[0]) == 1 and
                    abs(check.coor[1]-tile.coor[1]) == 1):
                    if (check.coor[0]-tile.coor[0] == -1 and
                            check.coor[1]-tile.coor[1] == -1):
                        tile.dirs['xym'] = check
                        tile.adjl.append(check)
                    elif (check.coor[0]-tile.coor[0] == 1 and
                            check.coor[1]-tile.coor[1] == 1):
                        tile.dirs['xyp'] = check
                        tile.adjl.append(check)
                    elif (check.coor[0]-tile.coor[0] == -1 and
                            check.coor[1]-tile.coor[1] == 1):
                        tile.dirs['yxm'] = check
                        tile.adjl.append(check)
                    elif (check.coor[0]-tile.coor[0] == 1 and
                            check.coor[1]-tile.coor[1] == -1):
                        tile.dirs['yxp'] = check
                        tile.adjl.append(check)
    @staticmethod
    def standon(tocheck, against):
        if (against.coor[0] == tocheck.x and 
            against.coor[1] == tocheck.y) :
            standon = True
        else: standon = False
        return standon
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
            Labels.playername_label.text = Typein.text
        Control.CurrentPlayer.name = Typein.text
    @staticmethod
    def on_key_press(symbol,modifiers):
        if symbol == key.ENTER:
            Labels.playername_label.text = Typein.text
            Typein.text =''
            GAME_WINDOW.pop_handlers()
            Control.handleraltered = False
        elif symbol == key.BACKSPACE:
            Typein.text = Typein.text[:-1]
            Labels.playername_label.text = Typein.text
        elif symbol:
            return True

Mapengine.levelgen()    
g_player = Player(coor=[1,1],img='pchar',id=1)
sp_player = Sp_Tile(x = ct(g_player.coor[0]),
                    y = ct(g_player.coor[1]), 
                    img = getim(g_player),id = g_player.id,
                    batch = player_batch)
List.g_players.append(g_player)
List.sp_overlays.append(sp_player)
Control = Control()
Control.CurrentPlayer = List.g_players[Control.inturn]
Control.sp_topath = Control.CurrentPlayer   
Control.goal = Control.CurrentPlayer
GAME_WINDOW.push_handlers(Control)
class Labels(object):
    @staticmethod
    def create(label,clean):
        clean.delete()
        Labels.playername_label = pyglet.text.Label(label, 
                                        'Courier_new',30,
                                        x= GAME_WINDOW.width,
                                        y = ROOMSIZEY*TILESIZE+25,
                                        anchor_x = 'right',
                                        anchor_y = 'center',
                                        batch = menu_batch)
    playername_label = pyglet.text.Label(Control.CurrentPlayer.name, 
                                        'Courier_new',30,
                                        x= GAME_WINDOW.width,
                                        y = ROOMSIZEY*TILESIZE+25,
                                        anchor_x = 'right',
                                        anchor_y = 'center', 
                                        batch = menu_batch)
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
            for genloc in List.g_tiles:
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
        List.sp_overlays[:] = [ol for ol in List.sp_overlays if
                               not det_ol(ol)]
    for sp_tile in List.sp_tiles:
        sp_tile.delete()
    del List.sp_tiles[:]
    del List.g_tiles[:]
def savelevel():
    savelev = open('saved_level','wb')
    cPickle.dump(List.g_tiles, savelev)
    cPickle.dump(List.g_players, savelev)
    savelev.close()     
def loadlevel(): 
    dellevel()
    for sp_overlay in List.sp_overlays:
        sp_overlay.delete()
    del List.sp_overlays[:]
    del List.g_players[:]
    loadlev = open('saved_level','rb')
    List.g_tiles = cPickle.load(loadlev)
    List.g_players = cPickle.load(loadlev)
    for g_tile in List.g_tiles:
        sp_tile = Sp_Tile(x=ct(g_tile.coor[0]), y=ct(g_tile.coor[1]), 
                          img=getim(g_tile),
                          batch= map_batch,id=g_tile.id)
        sp_tile._set_rotation(g_tile.rot)
        List.sp_tiles.append(sp_tile)
        if g_tile.overlays:
            for ol in g_tile.overlays:
                sp_overlay = Sp_Tile(x=ct(ol.x),y=ct(ol.y),
                                     img=getim(ol),
                                     batch=item_batch,id=ol.id,
                                     ol=True) 
                List.sp_overlays.append(sp_overlay)      
    for g_player in List.g_players:
        sp_overlay = Sp_Tile(x=ct(g_player.coor[0]),
                             y=ct(g_player.coor[1]),
                             img = getim(g_player),
                             id= g_player.id,
                             batch = player_batch)
        List.sp_overlays.append(sp_overlay)   
    loadlev.close()
    Control.turn()
def update(dt):
    if Path.anim == True:
        Anim.movetoward(Path.node.connect(),
                        Control.CurrentPlayer.connect())
@GAME_WINDOW.event
def on_draw():
    GAME_WINDOW.clear()
    map_batch.draw()
    debug_batch.draw()
    item_batch.draw()
    player_batch.draw()
    SelBuild.build_label.draw()
    Cursor.cursor.draw()
    menu_batch.draw()
@GAME_WINDOW.event
def on_resize(width, height):
    global TILESIZE
    global ANC_TILE
    global XSIZE
    global YSIZE
    if width - 50 > XSIZE or width + 50 < XSIZE:
        scaleto = float(width) / float(XSIZE)
        scaletoint = scaleto*10000
        scaletoint = int(scaletoint)
        scaletoint = float(scaletoint)/10000
        glScalef(scaletoint, scaletoint, scaletoint)
        TILESIZE = TILESIZE * scaletoint
        ANC_TILE = TILESIZE/2
        Cursor.cursor.x = Cursor.cursor.x * scaletoint
        Cursor.cursor.y = Cursor.cursor.y * scaletoint
        #Cursor.mposx = Cursor.mposx * scaletoint
        #Cursor.mposy = Cursor.mposy * scaletoint
        XSIZE = width*scaletoint
        YSIZE = height*scaletoint
    width = XSIZE
    height = YSIZE
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, (1.0/30.0))
    pyglet.app.run()
