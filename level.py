import gui
import tile
import cPickle
import random
import pyglet.window
import store


class Level(pyglet.window.Window):
    def __init__(self,x=10,y=10,tset=None):
        self.x = x
        self.y = y
        self.tset = tset
        super(Level, self).__init__(self.x * store.ts
                                  + store.ts * 3,
                                    self.y * store.ts
                                  + store.ts,
                                    resizable= False)
        self.xsize = self.width
        self.xcenter = self.xsize / 2
        self.ysize = self.height
        self.ycenter = self.ysize / 2
        self.buildmenu = gui.SelBuild(self)
    def on_draw(self):
        self.clear()
        store.map_bt.draw()
        store.debug_bt.draw()
        store.item_bt.draw()
        store.player_bt.draw()
        self.buildmenu.label.draw()
        store.cursor.sp.draw()
        store.menu_bt.draw()
    def on_resize(self,width,height):
        store.ts
        store.ats
        self.xsize
        self.ysize
        if width - 50 > self.xsize or width + 50 < self.xsize:
            scaleto = float(width) / float(self.xsize)
            scaletoint = scaleto*10000
            scaletoint = int(scaletoint)
            scaletoint = float(scaletoint)/10000
            glscalef(scaletoint, scaletoint, scaletoint)
            store.ts = store.ts * scaletoint
            store.ats = store.ts/2
            cursor.cursor.x = cursor.cursor.x * scaletoint
            cursor.cursor.y = cursor.cursor.y * scaletoint
            #cursor.mposx = cursor.mposx * scaletoint
            #cursor.mposy = cursor.mposy * scaletoint
            self.xsize = width*scaletoint
            self.ysize = height*scaletoint
        width = self.xsize
        height = self.ysize
    def levelgen(self): 
        if store.store['spt']: dellevel()
        self.levelarea = Gamearea(1,'level',
                             [[0,store.ts*self.x],
                             [0,store.ts*self.y]])
        gcoor = [0,0]
        genid = 1
        for i in range(self.x):
            store.add(ctile(gcoor,genid),'gt')
            genid +=1   
            for i in range(self.y-1):
                gcoor= [gcoor[0],gcoor[1] + 1]
                store.add(ctile(gcoor,genid),'gt')
                genid += 1
            gcoor= [gcoor[0],0]
            gcoor= [gcoor[0]+1,gcoor[1]]
        for tile in store.store['gt']:
            tile.interlace(store.store['gt'])
            sp_tile = self.buildmenu.build(tile,'space',
                                           tile.coor,tile.id)  
            if len(tile.adjl) != 8:
                sp_tile = self.buildmenu.build(tile,'wall',
                                               tile.coor)
class Gamearea(object):
    def __init__(self,id=None,name=None,coor=None):
        self.id = id
        self.name = name
        self.coor = coor
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
def adjlist(tocheck):
    adjlist = []
    for g_tile in tocheck.dirs.itervalues():
        if g_tile and g_tile.passable == False:
            adjlist.append(g_tile)
    for g_tile in tocheck.dirs.itervalues():
        if g_tile and g_tile.passable == False: 
            adjlist.append(g_tile)
    return adjlist
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
        toarrange.connect()._set_image(store.image['pil'])
        toarrange.img = 'pil'
        toarrange.tt = 's'
    elif xac == 1 and yac == 0:
        if (toarrange.dirs['xap'] and
            toarrange.dirs['xap'].passable == False):
            toarrange.connect()._set_image(store.image['cap'])
            toarrange.connect()._set_rotation(270)
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 270
        elif (toarrange.dirs['xam'] and 
            toarrange.dirs['xam'].passable == False):
            toarrange.connect()._set_image(store.image['cap'])
            toarrange.connect()._set_rotation(90)
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 90
    elif xac == 2 and yac == 0 :
        toarrange.connect()._set_rotation(90)
        toarrange.tt = 'x'
        toarrange.connect()._set_image(store.image['wall'])
        toarrange.img = 'wall'
        toarrange.rot = 90
    elif xac != 0 and yac != 0:
        if xac+yac == 2:
            toarrange.connect()._set_image(store.image['corner'])
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
            toarrange.connect()._set_image(store.image['tsect'])
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
            toarrange.connect()._set_image(store.image['fourway'])
            toarrange.img = 'fourway'
            toarrange.tt = 'fw'
    else: 
        if (yac == 1 and toarrange.dirs['yam'] and 
            toarrange.dirs['yam'].passable == False):
            toarrange.connect()._set_image(store.image['cap'])
            toarrange.connect()._set_rotation(0)
            toarrange.img = 'cap'
            toarrange.tt = 'xp_c'
            toarrange.rot = 0
        elif (yac == 1 and toarrange.dirs['yap'] and 
            toarrange.dirs['yap'].passable == False):
            toarrange.connect()._set_image(store.image['cap'])
            toarrange.connect()._set_rotation(180)
            toarrange.img = 'cap'
            toarrange.tt = 'xm_c'
            toarrange.rot = 180
        else:
            toarrange.tt = 'y'
            toarrange.connect()._set_image(store.image['wall'])
            toarrange.img = 'wall'
    if fit == True:
        fitnext(toarrange.wadjl)
def coll(direc):
    collision = False
    for g_tile in lists.g_tiles:
        if (g_tile.passable == False and
            g_tile.coor[1] == direc[0] and g_tile.coor[0] == direc[1]):
                collision = True
                return collision
    return collision
def fitnext(tile):
    for i in tile:
        i.wadjl = adjlist(i)
        arrange(i,False)
def ctile(gcoor,genid):
    var_space = ['space','space_v1','space','space_v2','space_v3']
    g_gen = tile.Tile(img=var_space[random.randint(0,
                   len(var_space)-1)],
                   id=genid,coor=gcoor,occup=False)  
    return g_gen
def standon(tocheck, against):
    if (against.coor[0] == tocheck.x and 
        against.coor[1] == tocheck.y) :
        standon = True
    else: standon = False
    return standon
def savelevel():
    savelev = open('saved_level','wb')
    cPickle.dump(lists.g_tiles, savelev)
    cPickle.dump(lists.g_players, savelev)
    savelev.close()     
def loadlevel(): 
    dellevel()
    for sp_overlay in lists.sp_overlays:
        sp_overlay.delete()
    del lists.sp_overlays[:]
    del lists.g_players[:]
    loadlev = open('saved_level','rb')
    lists.g_tiles = cPickle.load(loadlev)
    lists.g_players = cPickle.load(loadlev)
    for g_tile in lists.g_tiles:
        sp_tile = Sp_Tile(x=clevel.ct(g_tile.coor[0]), y=clevel.ct(g_tile.coor[1]), 
                          img=getim(g_tile),
                          bt= map_batch,id=g_tile.id)
        sp_tile._set_rotation(g_tile.rot)
        lists.sp_tiles.append(sp_tile)
        if g_tile.overlays:
            for ol in g_tile.overlays:
                sp_overlay = Sp_Tile(x=clevel.ct(ol.x),y=clevel.ct(ol.y),
                                     img=getim(ol),
                                     bt=item_batch,id=ol.id,
                                     ol=True) 
                lists.sp_overlays.append(sp_overlay)      
    for g_player in lists.g_players:
        sp_overlay = Sp_Tile(x=clevel.ct(g_player.coor[0]),
                             y=clevel.ct(g_player.coor[1]),
                             img = getim(g_player),
                             id= g_player.id,
                             bt = player_batch)
        lists.sp_overlays.append(sp_overlay)   
    loadlev.close()
    Control.turn()
def dellevel(delol=False):
    if delol == True:
        lists.sp_overlays[:] = [ol for ol in 
                               List.sp_overlays if not 
                               det_ol(ol)]
    for sp_tile in lists.sp_tiles:
        sp_tile.delete()
    del lists.sp_tiles[:]
    del lists.g_tiles[:]
